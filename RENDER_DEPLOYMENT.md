# 🚀 Deploying SDG Digital Twin Platform on Render

This guide walks you through deploying the **SDG Digital Twin & Future Impact Simulation Platform** on [Render](https://render.com), a modern cloud platform that makes deployment simple and automatic.

---

## 📋 Table of Contents

1. [Why Render?](#why-render)
2. [Prerequisites](#prerequisites)
3. [Deployment Options](#deployment-options)
4. [Option 1: Blueprint Deployment (Recommended)](#option-1-blueprint-deployment-recommended)
5. [Option 2: Manual Deployment](#option-2-manual-deployment)
6. [Configuration](#configuration)
7. [Post-Deployment](#post-deployment)
8. [Troubleshooting](#troubleshooting)

---

## 🎯 Why Render?

- **Free Tier**: Free PostgreSQL database + 750 hours/month of free web service time
- **Auto-Deploy**: Automatic deployments from Git
- **Zero Config**: Works out of the box with minimal configuration
- **PostgreSQL**: Free managed database (better than SQLite for production)
- **HTTPS**: Automatic SSL certificates
- **Easy Scaling**: Simple upgrade path when you need more resources

---

## ✅ Prerequisites

Before you begin, ensure you have:

1. **GitHub Account**: Your code should be in a GitHub repository
2. **Render Account**: Sign up at [render.com](https://render.com) (free)
3. **Git**: Your project pushed to GitHub

---

## 🎯 Deployment Options

### Option 1: Blueprint Deployment (Recommended) ⭐
Use the included `render.yaml` file for one-click deployment of all services.

### Option 2: Manual Deployment
Manually create each service through the Render dashboard.

---

## 🚀 Option 1: Blueprint Deployment (Recommended)

This is the **fastest and easiest** way to deploy!

### Step 1: Push to GitHub

```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### Step 2: Create New Blueprint

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub repository
4. Render will automatically detect `render.yaml`
5. Click **"Apply"**

### Step 3: Configure Environment Variables

Render will create all services automatically. You need to set a few environment variables:

**For Backend Service (`sdg-platform-backend`):**

| Variable | Value | Description |
|----------|-------|-------------|
| `SECRET_KEY` | (auto-generated) | JWT secret key |
| `DATABASE_URL` | (auto-linked) | PostgreSQL connection string |
| `CORS_ORIGINS` | Your frontend URL | e.g., `https://sdg-platform-frontend.onrender.com` |

### Step 4: Wait for Deployment

- Backend: ~5-10 minutes
- Database: ~2-3 minutes
- Frontend: ~1-2 minutes

✅ **Done!** Your app is live!

---

## 🔧 Option 2: Manual Deployment

If you prefer manual control, follow these steps:

### Step 1: Deploy PostgreSQL Database

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"PostgreSQL"**
3. Configure:
   - **Name**: `sdg-platform-db`
   - **Database**: `sdg_platform`
   - **User**: `sdg_user`
   - **Plan**: Free
4. Click **"Create Database"**
5. **Save the Internal Database URL** (you'll need it for the backend)

### Step 2: Deploy Backend API

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Configure:

| Setting | Value |
|---------|-------|
| **Name** | `sdg-platform-backend` |
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r backend/requirements.txt` |
| **Start Command** | `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT` |
| **Plan** | Free |

4. **Add Environment Variables**:

```bash
PYTHON_VERSION=3.9.16
DATABASE_URL=<your-database-internal-url>
SECRET_KEY=<generate-a-random-secure-key>
CORS_ORIGINS=*
```

5. Click **"Create Web Service"**

### Step 3: Deploy Frontend

1. Click **"New +"** → **"Static Site"**
2. Connect your GitHub repository
3. Configure:

| Setting | Value |
|---------|-------|
| **Name** | `sdg-platform-frontend` |
| **Build Command** | (leave empty) |
| **Publish Directory** | `frontend` |
| **Plan** | Free |

4. **Add Environment Variables**:

```bash
API_URL=<your-backend-url>
```

Example: `https://sdg-platform-backend.onrender.com`

5. Click **"Create Static Site"**

### Step 4: Update Frontend API URLs

Update your frontend files to use the Render backend URL:

**In `frontend/auth.js`, `frontend/dashboard.js`, etc.:**

```javascript
// Change from:
const API_URL = 'http://localhost:8000';

// To:
const API_URL = 'https://sdg-platform-backend.onrender.com';
```

**Or use environment variable:**

```javascript
const API_URL = window.ENV?.API_URL || 'https://sdg-platform-backend.onrender.com';
```

---

## ⚙️ Configuration

### Environment Variables Explained

#### Backend (`sdg-platform-backend`)

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `DATABASE_URL` | ✅ | PostgreSQL connection string | `postgresql://user:pass@host/db` |
| `SECRET_KEY` | ✅ | JWT signing key (use strong random value) | `your-super-secret-key-here` |
| `CORS_ORIGINS` | ✅ | Allowed frontend origins | `https://your-frontend.onrender.com` or `*` |
| `PYTHON_VERSION` | ⚠️ | Python version | `3.9.16` |

#### Frontend (`sdg-platform-frontend`)

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `API_URL` | ✅ | Backend API URL | `https://sdg-platform-backend.onrender.com` |

### Generating a Secure SECRET_KEY

```python
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Or use Render's auto-generation feature.

---

## 🎉 Post-Deployment

### Step 1: Verify Backend Health

Visit: `https://sdg-platform-backend.onrender.com/api/health`

Expected response:
```json
{
  "status": "healthy",
  "database": "connected"
}
```

### Step 2: Test Frontend

Visit: `https://sdg-platform-frontend.onrender.com`

You should see the landing page.

### Step 3: Create Admin User

Use the API docs to create your first user:
`https://sdg-platform-backend.onrender.com/docs`

Or use curl:

```bash
curl -X POST "https://sdg-platform-backend.onrender.com/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "email": "admin@example.com",
    "password": "SecurePass123!",
    "full_name": "Admin User"
  }'
```

### Step 4: Initialize Database

If your app needs database initialization:

```bash
# SSH into your backend service (available in Render dashboard)
cd backend
python -c "from database import init_db; init_db()"
```

---

## 🛠️ Troubleshooting

### Issue: Backend won't start

**Symptoms**: Service fails to start, shows "Deploy failed"

**Solutions**:
1. Check logs in Render dashboard
2. Verify `DATABASE_URL` is set correctly
3. Ensure all dependencies are in `requirements.txt`
4. Check Python version compatibility

```bash
# View logs
# Go to Render Dashboard → Your Service → Logs
```

### Issue: Database connection error

**Symptoms**: `psycopg2.OperationalError` or similar

**Solutions**:
1. Verify database is running (check Render dashboard)
2. Use the **Internal Database URL** (not external)
3. Update `backend/database.py` to support PostgreSQL:

```python
# backend/database.py
import os
from sqlalchemy import create_engine

DATABASE_URL = os.getenv("DATABASE_URL")

# Handle Render's postgres:// URL (need postgresql://)
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
```

### Issue: CORS errors in frontend

**Symptoms**: `Access-Control-Allow-Origin` errors in browser console

**Solutions**:
1. Set `CORS_ORIGINS` in backend environment variables
2. Update `backend/main.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

origins = os.getenv("CORS_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue: Frontend can't reach backend

**Symptoms**: API calls fail with network errors

**Solutions**:
1. Verify backend URL in frontend code
2. Check backend is deployed and running
3. Test backend health endpoint directly
4. Update all API URLs in frontend:

```javascript
// frontend/config.js (create this file)
const API_URL = 'https://sdg-platform-backend.onrender.com';
export default API_URL;
```

### Issue: Static files not loading

**Symptoms**: CSS/JS files return 404

**Solutions**:
1. Verify `Publish Directory` is set to `frontend`
2. Check file paths are relative, not absolute
3. Clear browser cache

### Issue: Free tier service sleeps

**Symptoms**: First request takes 30-60 seconds

**Explanation**: Render's free tier services sleep after 15 minutes of inactivity.

**Solutions**:
1. Upgrade to paid tier ($7/month for always-on)
2. Use a uptime monitoring service (e.g., UptimeRobot) to ping every 10 minutes
3. Accept the cold start delay

---

## 🔄 Auto-Deploy from Git

Render automatically deploys when you push to your main branch:

```bash
git add .
git commit -m "Update feature"
git push origin main
```

**Deployment triggers automatically!**

### Disable Auto-Deploy

In Render Dashboard → Service Settings → Build & Deploy:
- Uncheck "Auto-Deploy"

---

## 📊 Monitoring & Logs

### View Logs

1. Go to Render Dashboard
2. Click on your service
3. Click **"Logs"** tab
4. Real-time logs appear here

### Check Service Health

```bash
# Backend health
curl https://sdg-platform-backend.onrender.com/api/health

# Frontend
curl -I https://sdg-platform-frontend.onrender.com
```

---

## 💰 Cost Breakdown

| Service | Free Tier | Paid Tier |
|---------|-----------|-----------|
| Web Service | 750 hours/month | $7/month (always-on) |
| PostgreSQL | 1 GB storage, expires 90 days | $7/month (permanent) |
| Static Site | Unlimited | Free |

**Total Free**: $0/month (with limitations)
**Total Paid**: $14/month (production-ready)

---

## 🚀 Production Checklist

Before going live:

- [ ] Set strong `SECRET_KEY`
- [ ] Configure specific `CORS_ORIGINS` (not `*`)
- [ ] Use internal database URL
- [ ] Enable auto-deploy from main branch
- [ ] Set up custom domain (optional)
- [ ] Configure environment-specific settings
- [ ] Test all API endpoints
- [ ] Test authentication flow
- [ ] Verify database migrations work
- [ ] Set up monitoring/alerts
- [ ] Review security headers
- [ ] Enable HTTPS (automatic on Render)
- [ ] Backup database regularly

---

## 🔗 Useful Links

- [Render Documentation](https://render.com/docs)
- [Render Community Forum](https://community.render.com)
- [Render Status Page](https://status.render.com)
- [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/)

---

## 📞 Support

- **Render Support**: [support@render.com](mailto:support@render.com)
- **Documentation Issues**: Open an issue on GitHub
- **Community Help**: [Render Community](https://community.render.com)

---

## 🎯 Next Steps

After successful deployment:

1. ✅ Test all features thoroughly
2. 🔐 Set up proper authentication
3. 📊 Configure monitoring and alerts
4. 🌐 Add custom domain (optional)
5. 📈 Scale up as needed
6. 🔄 Set up CI/CD pipeline
7. 📦 Configure backup strategy

---

**Happy Deploying! 🚀**

Need help? Check the [troubleshooting section](#troubleshooting) or reach out to the Render community.
