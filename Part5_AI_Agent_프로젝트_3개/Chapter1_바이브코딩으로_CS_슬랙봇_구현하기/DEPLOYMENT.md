# Deployment Guide - Google Cloud Run

This guide will help you deploy the Slack Claude Bot to Google Cloud Run.

## Prerequisites

1. Google Cloud account
2. `gcloud` CLI installed and authenticated
3. Docker installed locally
4. Project: `fastcampus-slackbot` already exists in GCP

## Step 1: Authenticate with Google Cloud

```bash
# Authenticate with Google Cloud
gcloud auth login

# Set the project
gcloud config set project fastcampus-slackbot

# Configure Docker to use gcloud as credential helper
gcloud auth configure-docker
```

## Step 2: Enable Required APIs

```bash
# Enable Cloud Run API
gcloud services enable run.googleapis.com

# Enable Container Registry API
gcloud services enable containerregistry.googleapis.com

# Enable Artifact Registry API (recommended over Container Registry)
gcloud services enable artifactregistry.googleapis.com
```

## Step 3: Build and Push Docker Image

### Option A: Using Container Registry (gcr.io)

```bash
# Tag the image for Container Registry
docker tag slack-claude-bot:latest gcr.io/fastcampus-slackbot/slack-claude-bot:latest

# Push the image
docker push gcr.io/fastcampus-slackbot/slack-claude-bot:latest
```

### Option B: Using Artifact Registry (Recommended)

```bash
# Create Artifact Registry repository (one-time setup)
gcloud artifacts repositories create slack-bot-repo \
  --repository-format=docker \
  --location=us-central1 \
  --description="Slack Claude Bot Docker repository"

# Configure Docker authentication for Artifact Registry
gcloud auth configure-docker us-central1-docker.pkg.dev

# Tag the image
docker tag slack-claude-bot:latest \
  us-central1-docker.pkg.dev/fastcampus-slackbot/slack-bot-repo/slack-claude-bot:latest

# Push the image
docker push us-central1-docker.pkg.dev/fastcampus-slackbot/slack-bot-repo/slack-claude-bot:latest
```

## Step 4: Deploy to Cloud Run

**IMPORTANT**: Replace the environment variables with your actual Slack credentials before deploying.

### Deploy Command

```bash
gcloud run deploy slack-claude-bot \
  --image us-central1-docker.pkg.dev/fastcampus-slackbot/slack-bot-repo/slack-claude-bot:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars "SLACK_BOT_TOKEN=xoxb-YOUR-ACTUAL-TOKEN,SLACK_SIGNING_SECRET=YOUR-ACTUAL-SECRET" \
  --memory 512Mi \
  --min-instances 0 \
  --max-instances 3 \
  --timeout 60 \
  --port 8080
```

### Alternative: Using .env file (Secure)

For better security, you can set environment variables interactively:

```bash
# Deploy without environment variables first
gcloud run deploy slack-claude-bot \
  --image us-central1-docker.pkg.dev/fastcampus-slackbot/slack-bot-repo/slack-claude-bot:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 512Mi \
  --min-instances 0 \
  --max-instances 3 \
  --timeout 60 \
  --port 8080

# Then update environment variables using Cloud Console:
# 1. Go to https://console.cloud.google.com/run
# 2. Click on the service
# 3. Click "EDIT & DEPLOY NEW REVISION"
# 4. Go to "Variables & Secrets" tab
# 5. Add environment variables
```

## Step 5: Get Service URL

```bash
# Get the deployed service URL
gcloud run services describe slack-claude-bot \
  --platform managed \
  --region us-central1 \
  --format 'value(status.url)'
```

This will output something like:
```
https://slack-claude-bot-xxxxx-uc.a.run.app
```

## Step 6: Configure Slack App

1. Go to https://api.slack.com/apps
2. Create a new app using the manifest from `slack_manifest.json`
3. Replace `YOUR-CLOUD-RUN-URL` in the manifest with your actual Cloud Run URL
4. Or manually configure Event Subscriptions:
   - Request URL: `https://slack-claude-bot-xxxxx-uc.a.run.app/slack/events`
   - Subscribe to bot events: `app_mention`
5. Install the app to your workspace
6. Copy the Bot Token (starts with `xoxb-`) and Signing Secret
7. Update Cloud Run environment variables with these credentials

## Step 7: Update Environment Variables

After getting your Slack credentials:

```bash
gcloud run services update slack-claude-bot \
  --region us-central1 \
  --update-env-vars "SLACK_BOT_TOKEN=xoxb-YOUR-ACTUAL-TOKEN,SLACK_SIGNING_SECRET=YOUR-ACTUAL-SECRET"
```

## Verification

Test the deployment:

```bash
# Test health endpoint
curl https://YOUR-CLOUD-RUN-URL/health

# Expected response: {"status":"ok"}
```

In Slack:
1. Invite the bot to a channel: `/invite @Claude CS Bot`
2. Mention the bot: `@Claude CS Bot hello`
3. You should receive a "Hello! I'm Claude CS Bot. I'm ready to help you!" response

## Monitoring and Logs

```bash
# View recent logs
gcloud run logs read slack-claude-bot \
  --region us-central1 \
  --limit 50

# Stream logs in real-time
gcloud run logs tail slack-claude-bot \
  --region us-central1

# View logs in Cloud Console
# https://console.cloud.google.com/logs
```

## Troubleshooting

### Issue: URL Verification Challenge Fails

**Solution**: Make sure your Cloud Run service is deployed and the `/slack/events` endpoint is accessible.

```bash
# Test the endpoint
curl -X POST https://YOUR-CLOUD-RUN-URL/slack/events \
  -H "Content-Type: application/json" \
  -d '{"type": "url_verification", "challenge": "test_challenge"}'

# Expected: {"challenge":"test_challenge"}
```

### Issue: 403 Forbidden on Slack Events

**Solution**: Check that your `SLACK_SIGNING_SECRET` environment variable is correct.

### Issue: Container Crashes on Startup

**Solution**: Check logs and ensure all required environment variables are set.

```bash
gcloud run logs read slack-claude-bot --region us-central1 --limit 100
```

### Issue: Cold Start Timeout

**Solution**: Increase min instances (costs more):

```bash
gcloud run services update slack-claude-bot \
  --region us-central1 \
  --min-instances 1
```

## Cost Optimization

- **Min instances**: Set to 0 to avoid idle charges
- **Max instances**: Set to 3 to limit concurrent costs
- **Memory**: 512Mi is sufficient for Phase 1

Expected costs (with default settings):
- Free tier: 2 million requests/month
- After free tier: ~$0.40 per million requests
- Phase 1 usage: Should stay within free tier for moderate use

## Cleanup

To delete the deployment:

```bash
# Delete Cloud Run service
gcloud run services delete slack-claude-bot --region us-central1

# Delete Docker images from Artifact Registry
gcloud artifacts docker images delete \
  us-central1-docker.pkg.dev/fastcampus-slackbot/slack-bot-repo/slack-claude-bot:latest
```

## Next Steps

Once Phase 1 is deployed and working:
1. Verify URL verification challenge works
2. Test app_mention events
3. Check logs for any errors
4. Move on to Phase 2: Claude Agent SDK integration
