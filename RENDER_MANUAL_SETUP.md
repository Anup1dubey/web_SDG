# 🚀 Render Manual Deployment Guide (Separate Services)

Deploy your SDG Platform backend and frontend separately on Render's free tier with PostgreSQL.

---

## 📋 Overview

You'll create 3 separate services:
1. **PostgreSQL Database** (free)
2. **Backend Web Service** (Python/FastAPI)
3. **Frontend Static Site** (HTML/CSS/JS)

**Total Time**: ~15-20 minutes
**Cost**: $0 (Free tier)

---

## Step 1: Create PostgreSQL Database 🗄️

### 1.1 Go to Render Dashboard
- Visit [dashboard.render.com](https://dashboard.render.com)
- Make sure you're signed in

### 1.2 Create New PostgreSQL Database
1. Click **"New +"** button (top right)
2. Select **"PostgreSQL"**

### 1.3 Configure Database
Fill in the following:

| Field | Value |
|-------|-------|
| **Name** | `sdg-platform-db` |
| **Database** | `sdg_platform` |
| **User** | `sdg_user` |
| **Region** | Choose closest to you |
| **PostgreSQL Version** | 16 (latest) |
| **Plan** | **Free** |

### 1.4 Create Database
- Click **"Create Database"**
- Wait 2-3 minutes for provisioning

### 1.5 Save Database Connection Info
Once created, you'll see connection details. **IMPORTANT**: Copy these values:

- **Internal Database URL** (starts with `postgres://`)
- **External Database URL** (for local testing)

**⚠️ IMPORTANT**: Use the **Internal Database URL** for your backend service (it's faster and free!)

**Example Internal URL:**
```
postgres://sdg_user:xxxxxxxx@dpg-xxxxx-a/sdg_platform
```

---

## Step 2: Deploy Backend API 🐍

### 2.1 Create New Web Service
1. Click **"New +"** → **"Web Service"**
2. Choose **"Build and deploy from a Git repository"**
3. Click **"Next"**

### 2.2 Connect GitHub Repository
1. Click **"Connect account"** to authorize GitHub
2. Find your repository: `Anup1dubey/web_SDG`
3. Click **"Connect"**

### 2.3 Configure Backend Service

Fill in these settings:

| Field | Value |
|-------|-------|
| **Name** | `sdg-platform-backend` |
| **Region** | Same as database |
| **Branch** | `main` (or your default branch) |
| **Root Directory** | Leave empty |
| **Runtime** | **Python 3** |
| **Build Command** | `pip install -r backend/requirements.txt` |
| **Start Command** | `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT` |
| **Plan** | **Starter (Free)** |

### 2.4 Add Environment Variables

Click **"Advanced"** → **"Add Environment Variable"**

Add these 3 variables:

#### Variable 1: DATABASE_URL
- **Key**: `DATABASE_URL`
- **Value**: Paste the **Internal Database URL** from Step 1.5

**⚠️ IMPORTANT**: If the URL starts with `postgres://`, change it to `postgresql://`:
```
# Change this:
postgres://sdg_user:pass@host/db

# To this:
postgresql://sdg_user:pass@host/db
```

#### Variable 2: SECRET_KEY
- **Key**: `SECRET_KEY`
- **Value**: Generate a random secure key

**Generate SECRET_KEY:**
```bash
# On your computer, run:
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Example output:
# xK9mP2nQ5wR8vT1aB4cD7eF0gH3jL6mN9pR2sT5uV8wY
```

Copy the output and paste it as the value.

#### Variable 3: CORS_ORIGINS
- **Key**: `CORS_ORIGINS`
- **Value**: `*`

(We'll update this later with your frontend URL for better security)

### 2.5 Create Web Service
1. Click **"Create Web Service"**
2. Wait 5-10 minutes for deployment
3. Watch the logs for any errors

### 2.6 Verify Backend is Running

Once deployed, you'll get a URL like:
```
https://sdg-platform-backend.onrender.com
```

**Test it:**
1. Visit: `https://sdg-platform-backend.onrender.com/docs`
2. You should see the FastAPI documentation page ✅

**If you see errors**, check the logs:
- Click on your service
- Go to **"Logs"** tab
- Look for error messages

---

## Step 3: Deploy Frontend Static Site 🎨

### 3.1 Create New Static Site
1. Click **"New +"** → **"Static Site"**
2. Connect the same GitHub repository
3. Click **"Connect"**

### 3.2 Configure Frontend Service

| Field | Value |
|-------|-------|
| **Name** | `sdg-platform-frontend` |
| **Branch** | `main` |
| **Root Directory** | Leave empty |
| **Build Command** | Leave empty (or use: `echo "No build needed"`) |
| **Publish Directory** | `frontend` |

### 3.3 Add Environment Variable (Optional)

Click **"Advanced"** → **"Add Environment Variable"**

- **Key**: `API_URL`
- **Value**: `https://sdg-platform-backend.onrender.com` (your backend URL)

*Note: This is optional because `config.js` auto-detects the API URL*

### 3.4 Create Static Site
1. Click **"Create Static Site"**
2. Wait 1-2 minutes for deployment
3. You'll get a URL like: `https://sdg-platform-frontend.onrender.com`

---

## Step 4: Update Configuration 🔧

### 4.1 Update Backend CORS (Important for Security)

Now that you have your frontend URL, update the backend:

1. Go to your backend service in Render
2. Click **"Environment"** tab
3. Find `CORS_ORIGINS` variable
4. Change from `*` to your actual frontend URL:
   ```
   https://sdg-platform-frontend.onrender.com
   ```
5. Click **"Save Changes"**
6. Service will automatically redeploy

### 4.2 Verify Frontend Configuration

The frontend should automatically detect the backend URL, but verify:

1. Visit your frontend: `https://sdg-platform-frontend.onrender.com`
2. Open browser console (F12)
3. Look for: `API Base URL: https://sdg-platform-backend.onrender.com`

If you see a different URL, you may need to manually update it.

---

## Step 5: Test Your Deployment 🧪

### 5.1 Test Backend API
Visit: `https://sdg-platform-backend.onrender.com/docs`

Try these endpoints:
- `GET /api/health` - Should return `{"status": "healthy"}`
- `POST /auth/register` - Try creating a test account

### 5.2 Test Frontend
Visit: `https://sdg-platform-frontend.onrender.com`

1. **Landing Page**: Should load correctly
2. **Register**: Create a new account
3. **Login**: Log in with your account
4. **Dashboard**: Should show your dashboard

### 5.3 Check Database Connection
In the backend logs, you should see:
```
INFO:     Database connected successfully
```

---

## 📊 Your Deployment URLs

Save these for reference:

| Service | URL | Purpose |
|---------|-----|---------|
| **Frontend** | `https://sdg-platform-frontend.onrender.com` | User interface |
| **Backend** | `https://sdg-platform-backend.onrender.com` | API |
| **API Docs** | `https://sdg-platform-backend.onrender.com/docs` | Interactive API documentation |
| **Database** | Internal URL (not public) | PostgreSQL database |

---

## 🎛️ Managing Your Services

### View Logs
1. Go to Render Dashboard
2. Click on any service
3. Click **"Logs"** tab
4. See real-time logs

### Restart Service
1. Go to service page
2. Click **"Manual Deploy"** → **"Deploy latest commit"**

### Update Environment Variables
1. Go to service page
2. Click **"Environment"** tab
3. Edit variables
4. Click **"Save Changes"**
5. Service redeploys automatically

### Check Service Status
- **Green dot** = Service is running ✅
- **Yellow dot** = Service is deploying 🔄
- **Red dot** = Service has errors ❌

---

## 🐛 Troubleshooting

### Backend won't start

**Check logs for:**
```
ModuleNotFoundError: No module named 'xyz'
```
**Solution**: Add missing package to `backend/requirements.txt`

**Check logs for:**
```
psycopg2.OperationalError: could not connect to server
```
**Solution**: 
1. Verify `DATABASE_URL` is set correctly
2. Make sure URL starts with `postgresql://` (not `postgres://`)
3. Use the Internal Database URL

### Frontend shows blank page

**Solutions:**
1. Check if `frontend/` directory exists in your repo
2. Verify `Publish Directory` is set to `frontend`
3. Check browser console for errors (F12)

### CORS errors in browser console

**Error:**
```
Access to fetch at 'https://backend.onrender.com' from origin 'https://frontend.onrender.com' has been blocked by CORS policy
```

**Solution:**
1. Update backend `CORS_ORIGINS` environment variable
2. Set it to your frontend URL: `https://sdg-platform-frontend.onrender.com`
3. Or use `*` for testing (not secure for production)

### Database connection fails

**Check:**
1. Database is running (green dot)
2. Using Internal Database URL (not External)
3. URL format is `postgresql://` (not `postgres://`)

### Service is sleeping (taking 30+ seconds to respond)

**This is normal for free tier!**

Free tier services sleep after 15 minutes of inactivity.

**Solutions:**
1. Accept the delay (first request wakes it up)
2. Use [UptimeRobot](https://uptimerobot.com) to ping every 10 minutes
3. Upgrade to paid tier ($7/month) for always-on service

---

## 💰 Free Tier Limits

| Service | Free Tier Limit |
|---------|-----------------|
| **Web Services** | 750 hours/month per service |
| **Static Sites** | Unlimited |
| **PostgreSQL** | 1 GB storage, expires after 90 days |
| **Bandwidth** | 100 GB/month |

**Note**: With 2 services (backend + frontend), you get:
- Backend: 750 hours/month (25 days of 24/7 uptime)
- Frontend: Unlimited ✅
- Total cost: **$0** ✅

---

## 🚀 Next Steps

### ✅ Your app is now live! Here's what to do next:

1. **Test thoroughly** - Try all features
2. **Share your URLs** - Give them to users/testers
3. **Monitor logs** - Watch for errors
4. **Set up custom domain** (optional)
   - Go to service → Settings → Custom Domain
5. **Upgrade database** (when ready)
   - After 90 days, upgrade to paid ($7/month) to keep data

---

## 📈 Scaling to Production

When you're ready for production:

### Upgrade Backend ($7/month)
- Always-on (no sleep)
- More resources
- Better performance

### Upgrade Database ($7/month)
- Permanent storage (no expiration)
- Daily backups
- More storage (10 GB)

### Add Monitoring
- Set up health checks
- Configure alerts
- Monitor uptime

**Total production cost: $14/month** 💵

---

## 🔗 Useful Links

- **Render Dashboard**: https://dashboard.render.com
- **Render Docs**: https://render.com/docs
- **Render Status**: https://status.render.com
- **Community Forum**: https://community.render.com

---

## 📞 Need Help?

- **Check logs first** - Most issues are visible in logs
- **Review this guide** - Common issues covered in troubleshooting
- **Render Community** - Ask questions at community.render.com
- **GitHub Issues** - Report bugs in your repository

---

**Congratulations! You've successfully deployed your SDG Platform on Render! 🎉**

*Happy building! 🌍*
