# Slack Claude Bot Project

## Project Overview
An AI-powered Slack bot that responds to user mentions using Claude AI with context from Notion knowledge base. The bot maintains thread conversation history and deploys to Google Cloud Run as a serverless application.

### Key Features
- Responds to `@slackbot` mentions with Claude AI
- Maintains thread conversation context (up to 15 messages)
- Searches Notion knowledge base via MCP integration
- Serverless deployment on Google Cloud Run
- Background task processing to meet Slack's 3-second timeout

### Architecture
```
Slack Event Subscription → Cloud Run (FastAPI) → Slack Web API
                                ↓
                      Claude Agent SDK (Haiku 4.5)
                                ↓
                       Notion MCP (optional tool call)
```

## Technology Stack
- **Language**: Python 3.11+
- **Web Framework**: FastAPI
- **LLM**: Claude Agent SDK (claude-haiku-4.5-20251015)
- **Package Manager**: uv (pip is prohibited)
- **Container**: Docker
- **Deployment**: Google Cloud Run
- **Slack Library**: slack_sdk
- **MCP**: Notion MCP

## Development Environment Setup

### Prerequisites
- Python 3.11 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- Docker (for containerization)
- Google Cloud SDK (for deployment)
- ngrok (for local development)

### Installation

1. **Install uv package manager**:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. **Clone and setup project**:
```bash
cd /path/to/project
uv sync
```

3. **Create environment file**:
```bash
cp .env.example .env
# Edit .env with your credentials
```

### Environment Variables
Create a `.env` file with the following variables:
```bash
SLACK_BOT_TOKEN=xoxb-...
SLACK_SIGNING_SECRET=...
ANTHROPIC_API_KEY=sk-ant-...
NOTION_API_KEY=secret_...
NOTION_DATABASE_ID=...
```

## Common Commands

### Development
```bash
# Run FastAPI app locally
uv run uvicorn main:app --reload --port 8000

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=.

# Expose local server via ngrok
ngrok http 8000
```

### Docker
```bash
# Build Docker image for AMD64 (required for Cloud Run)
docker build --platform linux/amd64 -t slack-claude-bot:latest .

# Run container locally
docker run -p 8080:8080 --env-file .env slack-claude-bot:latest
```

### Google Cloud Run Deployment

#### Complete Deployment Steps

```bash
# 1. Set project (replace with your project ID)
gcloud config set project youtube-mcp-473606

# 2. Enable required APIs
gcloud services enable run.googleapis.com artifactregistry.googleapis.com

# 3. Create Artifact Registry repository (one-time setup)
gcloud artifacts repositories create slack-bot-repo \
  --repository-format=docker \
  --location=us-central1 \
  --description="Slack Claude Bot Docker repository"

# 4. Configure Docker authentication
gcloud auth configure-docker us-central1-docker.pkg.dev --quiet

# 5. Build Docker image for AMD64 (IMPORTANT for Cloud Run)
# Note: Cloud Run requires linux/amd64 architecture
docker build --platform linux/amd64 -t slack-claude-bot:latest .

# 6. Tag image for Artifact Registry
docker tag slack-claude-bot:latest \
  us-central1-docker.pkg.dev/youtube-mcp-473606/slack-bot-repo/slack-claude-bot:latest

# 7. Push image to Artifact Registry
docker push us-central1-docker.pkg.dev/youtube-mcp-473606/slack-bot-repo/slack-claude-bot:latest

# 8. Deploy to Cloud Run
gcloud run deploy slack-claude-bot \
  --image us-central1-docker.pkg.dev/youtube-mcp-473606/slack-bot-repo/slack-claude-bot:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars "SLACK_BOT_TOKEN=xoxb-...,SLACK_SIGNING_SECRET=..." \
  --memory 512Mi \
  --min-instances 0 \
  --max-instances 3 \
  --timeout 60 \
  --port 8080 \
  --project youtube-mcp-473606

# 9. Get service URL
gcloud run services describe slack-claude-bot \
  --region us-central1 \
  --format 'value(status.url)'

# 10. Test health endpoint
curl https://slack-claude-bot-806381030765.us-central1.run.app/health
# Expected: {"status":"ok"}
```

#### Deployed Service Information

- **Service URL**: `https://slack-claude-bot-806381030765.us-central1.run.app`
- **Project**: `youtube-mcp-473606`
- **Region**: `us-central1`
- **Slack Events URL**: `https://slack-claude-bot-806381030765.us-central1.run.app/slack/events`

### Package Management
```bash
# Add new package
uv add package-name

# Add dev dependency
uv add --dev package-name

# Update dependencies
uv sync

# Show installed packages
uv pip list
```

### Testing Slack Events

#### Method 1: Python Test Script
```bash
python3 test_slack_event.py
```

#### Method 2: Curl Test Script
```bash
./test_with_curl.sh
```

These scripts simulate Slack app_mention events with valid signatures to test the deployed bot without needing to post in actual Slack channels.

**Test files included:**
- `test_slack_event.py` - Python script with detailed output
- `test_with_curl.sh` - Bash script using curl

## Project Constraints
- **Keep it simple**: Educational project, avoid production-level complexity
- **Prohibited**:
  - Pub-Sub architecture
  - Secrets Manager (use .env instead)
  - Redis, Celery
  - Slack Socket Mode
- **Allowed**:
  - Synchronous processing
  - Simple background tasks (FastAPI BackgroundTasks or asyncio.create_task)

## Development Phases

### Phase 1: Hello Bot + Event Subscriptions ✅
- ✅ Deploy simple "Hello" bot to Cloud Run
- ✅ Setup Slack Event Subscriptions
- ✅ Handle URL verification challenge
- ✅ Respond to mentions with static message

**Status**: COMPLETED

### Phase 2: Claude Agent SDK Integration ✅
- ✅ Connect Claude AI for dynamic responses
- ✅ Implement thread context management (up to 15 messages)
- ✅ Add "Thinking..." → final response flow
- ✅ Error handling and retry logic
- ✅ Token counting and performance metrics
- ✅ Background task processing

**Status**: COMPLETED
**Documentation**: See `PHASE2_COMPLETION.md` for details

**Key Features:**
- Model: `claude-haiku-4.5-20251015`
- Thread history: Up to 15 messages
- Response includes: Processing time, input/output tokens
- Graceful error handling with user-friendly messages

### Phase 3: Notion MCP Integration 🚧
- Setup Notion MCP server
- Register MCP tools with Claude Agent SDK
- Display tool usage in thread
- Add knowledge source attribution

**Status**: PENDING

## Key Reference Links
- [Claude Agent SDK](https://github.com/anthropics/claude-agent-sdk-python)
- [Slack Events API](https://api.slack.com/events-api)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Google Cloud Run Docs](https://cloud.google.com/run/docs)
- [uv Package Manager](https://github.com/astral-sh/uv)

---

# Development Guidelines

## 1. TDD (Test-Driven Development)
- Follow TDD principles for all development
- Write tests first before implementing features
- Ensure tests define the expected behavior clearly

## 2. Test Execution
- **MUST** run tests after every implementation
- Verify all tests pass before moving to the next task
- Fix any failing tests immediately

## 3. Atomic Commits
- Commit after each logical unit of implementation
- Follow atomic commit principles - one logical change per commit
- Keep commits small and focused on a single purpose

## 4. Selective File Staging
- Only `git add` files that are related to the current commit
- Do not stage unrelated changes
- Review staged files before committing

## 5. No Push Policy
- **NEVER** execute `git push`
- All changes remain local only
- User will handle remote repository operations

---

# Deployment Troubleshooting

## Docker Architecture Mismatch (M1/M2/M3 Mac)

**Solution:**
```bash
# Always build with AMD64 platform for Cloud Run
docker build --platform linux/amd64 -t slack-claude-bot:latest .
docker tag slack-claude-bot:latest us-central1-docker.pkg.dev/PROJECT_ID/REPO/slack-claude-bot:latest
docker push us-central1-docker.pkg.dev/PROJECT_ID/REPO/slack-claude-bot:latest
```

## Billing Not Enabled

**Solution:**
```bash
# Option 1: Link billing in console
# https://console.cloud.google.com/billing → Link a billing account

# Option 2: Switch to a project with billing
gcloud config set project PROJECT_ID_WITH_BILLING
```

## Authentication Failed

**Solution:**
```bash
gcloud auth login
gcloud auth configure-docker us-central1-docker.pkg.dev
```

## Container Startup Failure

**Solution:**
```bash
# Test locally first
docker run -p 8080:8080 --env-file .env slack-claude-bot:latest

# Check dependencies
uv sync
```

## Environment Variables Not Set

**Solution:**
```bash
gcloud run services update slack-claude-bot \
  --region us-central1 \
  --set-env-vars "SLACK_BOT_TOKEN=xoxb-...,SLACK_SIGNING_SECRET=..."
```

## View Logs

### Method 1: Cloud Logging (Recommended)

```bash
# View recent logs (last 10 minutes)
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=slack-claude-bot" \
  --limit 20 \
  --project youtube-mcp-473606 \
  --format="table(timestamp,severity,textPayload)" \
  --freshness=10m

# View logs with specific severity
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=slack-claude-bot AND severity>=ERROR" \
  --limit 20 \
  --project youtube-mcp-473606 \
  --format="table(timestamp,severity,textPayload)" \
  --freshness=1h

# View logs in JSON format for detailed inspection
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=slack-claude-bot" \
  --limit 10 \
  --project youtube-mcp-473606 \
  --format=json \
  --freshness=10m

# Stream real-time logs (follow mode)
gcloud logging tail "resource.type=cloud_run_revision AND resource.labels.service_name=slack-claude-bot" \
  --project youtube-mcp-473606
```

### Method 2: Cloud Console (Web UI)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to **Cloud Run** → **slack-claude-bot**
3. Click on **LOGS** tab
4. Use the query builder or enter filter:
   ```
   resource.type="cloud_run_revision"
   resource.labels.service_name="slack-claude-bot"
   ```

### Method 3: Check Service Status

```bash
# Get service details
gcloud run services describe slack-claude-bot \
  --region us-central1 \
  --project youtube-mcp-473606

# Get service status in YAML format
gcloud run services describe slack-claude-bot \
  --region us-central1 \
  --project youtube-mcp-473606 \
  --format yaml

# List all revisions
gcloud run revisions list \
  --service slack-claude-bot \
  --region us-central1 \
  --project youtube-mcp-473606
```

### Common Log Filters

```bash
# Filter by time range (last 1 hour)
--freshness=1h

# Filter by time range (last 30 minutes)
--freshness=30m

# Filter by severity
AND severity>=WARNING
AND severity>=ERROR

# Filter by specific text in logs
AND textPayload:"app_mention"
AND textPayload:"error"

# Combine filters
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=slack-claude-bot AND severity>=ERROR" \
  --limit 50 \
  --project youtube-mcp-473606 \
  --freshness=1h
```

### Useful Log Queries for Debugging

```bash
# Check if Claude API calls are succeeding
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=slack-claude-bot AND textPayload:\"anthropic.com\"" \
  --limit 10 \
  --project youtube-mcp-473606 \
  --freshness=10m

# Check Slack event processing
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=slack-claude-bot AND textPayload:\"/slack/events\"" \
  --limit 10 \
  --project youtube-mcp-473606 \
  --freshness=10m

# Check for errors only
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=slack-claude-bot AND severity>=ERROR" \
  --limit 50 \
  --project youtube-mcp-473606 \
  --freshness=1h \
  --format="table(timestamp,severity,textPayload)"
```
