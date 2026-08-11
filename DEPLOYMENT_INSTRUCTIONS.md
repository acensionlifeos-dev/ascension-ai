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
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn src.serving.api:app --host 0.0.0.0 --port $PORT`

### 4. Environment Variables
No additional environment variables needed for demo mode.

### 5. Deploy
Click "Create Web Service"

## Expected URL
Once deployed, the AI will be available at:
`https://ascension-ai.onrender.com`

## What You'll See
- Beautiful gradient interface
- AI generation capability
- Model information
- Stats showing 100M parameters, 100TB+ training data, 0 external APIs

## This Is The AI That Will Power Ascension

This deployment is the foundation for the AI that will eventually:
- Power the Ascension LifeOS system
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
