# Ascension AI - Render Deployment Instructions

## Manual Deployment Steps

Since the Render CLI is not installed, deploy via the Render dashboard:

### 1. Go to Render Dashboard
Visit: https://dashboard.render.com

### 2. Create New Web Service
- Click "New" → "Web Service"
- Connect to GitHub repository: `acensionlifeos-dev/ascension-ai`
- Select branch: `master`

### 3. Configure Service
- **Name**: `ascension-ai`
- **Region**: Oregon (or closest to you)
- **Runtime**: Python 3
- **Build Command**: `pip install -r requirements.txt && python scripts/download_model.py`
- **Start Command**: `uvicorn src.serving.api:app --host 0.0.0.0 --port $PORT`

### 4. Environment Variables
- `ASCENSION_AI_TEST_TOKEN`: private code for the standalone test screen.
- `ASCENSION_AI_SERVICE_TOKEN`: separate private code for future LifeOS and Nexus server-to-server calls.
- `ASCENSION_MODEL_PROFILE`: `starter`, `standard`, or `pro`.
- `ASCENSION_AI_ALLOWED_ORIGINS`: `https://ascensionlifeos.onrender.com` if the protected browser lab will be accessed cross-origin.
- Start with `starter` on a 512 MB service. After upgrading the AI service to Render Pro, change this to `pro` and redeploy.

### 5. Deploy
Click "Create Web Service"

## Expected URL
Once deployed, the AI will be available at:
`https://ascension-ai.onrender.com`

## What You'll See
- Private ChatGPT-style test interface
- Selectable AP, LifeOS, NexusHome, NexusFamily, and neutral-core shells
- Local model and runtime status
- No hosted AI provider calls

## This Is The AI That Will Power Ascension

This deployment is the native foundation wired to:
- Power AP chat and router-backed LifeOS intelligence when the LifeOS service enables native routing
- Surface direct intelligence inside Creation workspaces
- Replace external AI dependencies
- Provide true multi-modal capabilities
- Run entirely on our infrastructure

## Post-Deployment

After deployment, you can:
1. Test the generation interface
2. Check the health endpoint: `/health`
3. View model info: `/model/info`
4. Use the API for programmatic access

This is the first step to having our own AI running our own system.
