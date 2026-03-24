# PathPilot Deployment Guide

This guide covers deploying PathPilot AI with:
- **Backend**: Render (Python/Flask)
- **Frontend**: Vercel (Static files)

---

## Important Considerations

### AI in Production
The original app uses **Ollama** (local LLM) which cannot run on Render. I've created:
1. **Fallback AI** (`fallback_ai.py`) - Provides basic responses without AI
2. **Production config** - Uses fallback mode automatically

### For Full AI Features
To keep AI features, you have two options:
1. **Use external Ollama service** - Deploy Ollama on a GPU server and set `OLLAMA_BASE_URL`
2. **Use external AI API** - Integrate OpenAI/Anthropic API (requires code changes)

---

## Step 1: Prepare Backend for Render

### Files Created:
- `app_production.py` - Optimized Flask app
- `config_production.py` - Production config
- `data_store_production.py` - Memory-based storage
- `fallback_ai.py` - Fallback AI engine
- `requirements_production.txt` - Minimal dependencies
- `render.yaml` - Render configuration

### Update render.yaml with your backend URL:
```yaml
# Edit render.yaml and replace 'your-backend.onrender.com' with your actual backend URL
```

---

## Step 2: Deploy Backend to Render

### Option A: Using render.yaml (Automatic)
1. Push your code to GitHub
2. Go to [Render Dashboard](https://dashboard.render.com)
3. Click "New" → "Web Service"
4. Connect your GitHub repository
5. Configure:
   - Name: `pathpilot-backend`
   - Region: Oregon (or closest to you)
   - Build Command: `pip install -r requirements_production.txt --no-cache-dir`
   - Start Command: `python -c "from app_production import app; app.run(host='0.0.0.0', port=\$PORT)"`
6. Add Environment Variables:
   - `FLASK_ENV`: `production`
   - `FLASK_SECRET_KEY`: (generate a secure key)
   - `USE_FALLBACK_AI`: `true`
   - `DATA_STORE_TYPE`: `memory`
   - `PYTHONUNBUFFERED`: `1`
7. Click "Create Web Service"

### Option B: Manual Deployment
1. Push code to GitHub
2. In Render dashboard:
   - New → Web Service
   - Select your repo
   - Set build/start commands as above
   - Add environment variables
   - Deploy

### Get Your Backend URL:
After deployment, you'll get a URL like: `https://pathpilot-backend.onrender.com`

---

## Step 3: Deploy Frontend to Vercel

### Option A: Deploy Static Frontend
1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "Add New..." → "Project"
3. Import your GitHub repository
4. Configure:
   - Framework Preset: `Other`
   - Build Command: `echo "No build required"`
   - Output Directory: `frontend-dist`
5. Click "Deploy"

### Option B: Using Vercel CLI
```bash
npm i -g vercel
vercel login
cd your-project
vercel
```

### Update Frontend with Backend URL:
After getting your Render backend URL, update:
1. `vercel.json` - Update the API proxy destination
2. `frontend-dist/index.html` - Replace `your-backend.onrender.com` with actual URL

---

## Step 4: Verify Deployment

### Health Check
Visit: `https://your-backend.onrender.com/health`

Expected response:
```json
{
  "status": "healthy",
  "ai_mode": "fallback",
  "store_type": "memory"
}
```

### Test the App
1. Visit your Vercel URL (frontend)
2. Click "Launch App"
3. Should redirect to Render backend
4. Test creating a profile and roadmap

---

## Environment Variables Reference

### Render Backend
| Variable | Value | Description |
|----------|-------|-------------|
| `FLASK_ENV` | `production` | Run in production mode |
| `FLASK_SECRET_KEY` | (generate) | Secret key for sessions |
| `USE_FALLBACK_AI` | `true` | Use fallback AI |
| `DATA_STORE_TYPE` | `memory` | Use in-memory storage |
| `OLLAMA_BASE_URL` | (optional) | External Ollama URL |
| `OLLAMA_MODEL` | (optional) | Ollama model name |

---

## Troubleshooting

### Common Issues

**1. "Module not found" errors**
- Make sure `requirements_production.txt` is correct
- Check that all imports in `app_production.py` are available

**2. "Session not working"**
- Ensure `FLASK_SECRET_KEY` is set
- Check CORS settings

**3. "Data not persisting"**
- This is expected with `DATA_STORE_TYPE=memory`
- Data resets on each deployment/restart
- For persistence, use a database (PostgreSQL, MongoDB)

**4. "AI not working"**
- Fallback AI provides basic responses
- For real AI, deploy Ollama externally or use OpenAI API

---

## Optional: Add Database Persistence

To persist data, add a PostgreSQL database:

1. Create PostgreSQL service on Render
2. Update `data_store_production.py` to use SQLAlchemy
3. Add database URL to environment variables:
   - `DATABASE_URL`: `postgres://user:pass@host/dbname`

---

## Architecture Overview

```
┌─────────────────┐     ┌──────────────────┐
│   Vercel        │────▶│   Render Backend │
│  (Frontend)     │     │   (Python/Flask)  │
│                │     │                   │
│ Static HTML    │     │ - API Routes      │
│ Tailwind CSS   │     │ - Fallback AI     │
│ JavaScript     │     │ - Session Mgmt    │
└─────────────────┘     └──────────────────┘
```

---

## Files Summary

| File | Purpose |
|------|---------|
| `app_production.py` | Main Flask app for production |
| `config_production.py` | Production configuration |
| `data_store_production.py` | Memory-based data storage |
| `fallback_ai.py` | Fallback AI without Ollama |
| `requirements_production.txt` | Production dependencies |
| `render.yaml` | Render deployment config |
| `vercel.json` | Vercel configuration |
| `frontend-dist/` | Static frontend files |

---

## Next Steps

1. Deploy backend to Render
2. Get backend URL
3. Update frontend files with backend URL
4. Deploy frontend to Vercel
5. Test the application
6. (Optional) Add PostgreSQL for data persistence
7. (Optional) Add external Ollama for AI features

