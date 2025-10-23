#!/bin/bash
#
# Deployment script for Slack Claude Bot to Google Cloud Run
# Project: fastcampus-slackbot
#

set -e  # Exit on error

# Configuration
PROJECT_ID="fastcampus-slackbot"
SERVICE_NAME="slack-claude-bot"
REGION="us-central1"
REPO_NAME="slack-bot-repo"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Slack Claude Bot Deployment ===${NC}"
echo

# Step 1: Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}Error: gcloud CLI is not installed${NC}"
    echo "Please install it from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Step 2: Check authentication
echo -e "${YELLOW}Checking authentication...${NC}"
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" &> /dev/null; then
    echo -e "${RED}Not authenticated with gcloud${NC}"
    echo "Please run: gcloud auth login"
    exit 1
fi
echo -e "${GREEN}✓ Authenticated${NC}"

# Step 3: Set project
echo -e "${YELLOW}Setting project to ${PROJECT_ID}...${NC}"
gcloud config set project ${PROJECT_ID}
echo -e "${GREEN}✓ Project set${NC}"

# Step 4: Enable required APIs
echo -e "${YELLOW}Enabling required APIs...${NC}"
gcloud services enable run.googleapis.com
gcloud services enable artifactregistry.googleapis.com
echo -e "${GREEN}✓ APIs enabled${NC}"

# Step 5: Create Artifact Registry repository (if doesn't exist)
echo -e "${YELLOW}Creating Artifact Registry repository...${NC}"
if ! gcloud artifacts repositories describe ${REPO_NAME} \
    --location=${REGION} &> /dev/null; then
    gcloud artifacts repositories create ${REPO_NAME} \
        --repository-format=docker \
        --location=${REGION} \
        --description="Slack Claude Bot Docker repository"
    echo -e "${GREEN}✓ Repository created${NC}"
else
    echo -e "${GREEN}✓ Repository already exists${NC}"
fi

# Step 6: Configure Docker authentication
echo -e "${YELLOW}Configuring Docker authentication...${NC}"
gcloud auth configure-docker ${REGION}-docker.pkg.dev --quiet
echo -e "${GREEN}✓ Docker configured${NC}"

# Step 7: Build Docker image for AMD64 (Cloud Run requirement)
echo -e "${YELLOW}Building Docker image for AMD64 architecture...${NC}"
echo -e "${YELLOW}Note: Cloud Run requires linux/amd64, not ARM64${NC}"
docker build --platform linux/amd64 -t ${SERVICE_NAME}:latest .
echo -e "${GREEN}✓ Image built${NC}"

# Step 8: Tag and push image
IMAGE_URL="${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${SERVICE_NAME}:latest"
echo -e "${YELLOW}Tagging and pushing image to ${IMAGE_URL}...${NC}"
docker tag ${SERVICE_NAME}:latest ${IMAGE_URL}
docker push ${IMAGE_URL}
echo -e "${GREEN}✓ Image pushed${NC}"

# Step 9: Get environment variables
echo
echo -e "${YELLOW}=== Environment Variables ===${NC}"
echo "Please provide your Slack credentials:"
echo

read -p "Enter SLACK_BOT_TOKEN (starts with xoxb-): " SLACK_BOT_TOKEN
read -p "Enter SLACK_SIGNING_SECRET: " SLACK_SIGNING_SECRET

if [ -z "$SLACK_BOT_TOKEN" ] || [ -z "$SLACK_SIGNING_SECRET" ]; then
    echo -e "${RED}Error: Environment variables cannot be empty${NC}"
    exit 1
fi

# Step 10: Deploy to Cloud Run
echo
echo -e "${YELLOW}Deploying to Cloud Run...${NC}"
gcloud run deploy ${SERVICE_NAME} \
    --image ${IMAGE_URL} \
    --platform managed \
    --region ${REGION} \
    --allow-unauthenticated \
    --set-env-vars "SLACK_BOT_TOKEN=${SLACK_BOT_TOKEN},SLACK_SIGNING_SECRET=${SLACK_SIGNING_SECRET}" \
    --memory 512Mi \
    --min-instances 0 \
    --max-instances 3 \
    --timeout 60 \
    --port 8080

echo -e "${GREEN}✓ Deployment complete!${NC}"

# Step 11: Get service URL
echo
echo -e "${YELLOW}=== Service Information ===${NC}"
SERVICE_URL=$(gcloud run services describe ${SERVICE_NAME} \
    --platform managed \
    --region ${REGION} \
    --format 'value(status.url)')

echo -e "${GREEN}Service URL: ${SERVICE_URL}${NC}"
echo
echo -e "${YELLOW}=== Next Steps ===${NC}"
echo "1. Test health endpoint: curl ${SERVICE_URL}/health"
echo "2. Configure Slack Event Subscriptions URL: ${SERVICE_URL}/slack/events"
echo "3. Subscribe to bot event: app_mention"
echo "4. Test in Slack: @Claude CS Bot hello"
echo
echo -e "${GREEN}Deployment successful! 🎉${NC}"
