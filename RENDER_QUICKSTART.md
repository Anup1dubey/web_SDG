# 🚀 Render Deployment - Quick Start Guide

Deploy your SDG Digital Twin Platform to Render in **under 10 minutes**!

## 📋 Prerequisites

- GitHub account with your code pushed
- Render account (sign up free at [render.com](https://render.com))

## ⚡ Quick Deploy Steps

### Option A: Blueprint (Recommended - 1 Click!) ⭐

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Ready for Render"
   git push
   ```

2. **Deploy on Render**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click **"New +"** → **"Blueprint"**
   - Connect your GitHub repo
   - Click **"Apply"**

3. **Done!** 🎉
   - Backend: `https://sdg-platform-backend.onrender.com`
   - Frontend: `https://sdg-platform-frontend.onrender.com`

### Option B: Manual Setup (More Control)

#### 1. Create PostgreSQL Database
- New + → PostgreSQL
- Name: `sdg-platform-db`
- Plan: Free
- Save the **Internal Database URL**

#### 2. Deploy Backend
- New + → Web Service
- Runtime: Python 3
- Build: `pip install -r backend/requirements.txt`
- Start: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
- Environment Variables:
  ```
  DATABASE_URL=<your-internal-db-url>
  SECRET_KEY=<generate-random-key>
  CORS_ORIGINS=*
  ```

#### 3. Deploy Frontend
- New + → Static Site
- Publish Directory: `frontend`
- No build command needed

## 🔑 Environment Variables

### Backend
| Variable | Value | How to Get |
|----------|-------|------------|
| `DATABASE_URL` | Auto-linked from DB | Render provides this |
| `SECRET_KEY` | Random string | Run: `python -c "import secrets; print(secrets.token_urlsafe(32))"` |
| `CORS_ORIGINS` | `*` (or your frontend URL) | Use `*` for testing |

### Frontend
| Variable | Value |
|----------|-------|
| `API_URL` | Your backend URL | e.g., `https://sdg-platform-backend.onrender.com` |

## ✅ Verify Deployment

1. **Check Backend**: Visit `https://your-backend.onrender.com/docs`
2. **Check Frontend**: Visit `https://your-frontend.onrender.com`
3. **Create Account**: Register and login!

## 🐛 Common Issues

### Backend won't start
- Check logs in Render dashboard
- Verify `DATABASE_URL` is set
- Make sure database is running

### CORS errors
- Set `CORS_ORIGINS` in backend environment variables
- Or use `*` for development

### Database connection fails
- Use the **Internal** database URL (not external)
- Wait for database to finish initializing (~2-3 minutes)

## 📚 More Help

- Full guide: See `RENDER_DEPLOYMENT.md`
- Render docs: [render.com/docs](https://render.com/docs)
- Issues? Check the troubleshooting section in the full guide

## 💡 Tips

- **Free tier** services sleep after 15 minutes of inactivity
- First request after sleep takes ~30-60 seconds
- Upgrade to paid ($7/month) for always-on service
- Use [UptimeRobot](https://uptimerobot.com) to ping your app and keep it awake

---

**That's it! Your platform is now live on Render! 🎉**
