# 🎯 Render Deployment - Step by Step Checklist

Follow this checklist to deploy your SDG Platform on Render with separate backend, frontend, and PostgreSQL database.

---

## ✅ Pre-Deployment Checklist

- [ ] Code is pushed to GitHub
- [ ] You have a Render account (sign up at [render.com](https://render.com))
- [ ] You're logged into Render dashboard

---

## 📝 Step-by-Step Deployment

### STEP 1: Create PostgreSQL Database (5 minutes) 🗄️

1. [ ] Go to [dashboard.render.com](https://dashboard.render.com)
2. [ ] Click **"New +"** → **"PostgreSQL"**
3. [ ] Fill in:
   - **Name**: `sdg-platform-db`
   - **Database**: `sdg_platform`
   - **User**: `sdg_user`
   - **Region**: (Choose closest to you)
   - **PostgreSQL Version**: 16
   - **Plan**: **Free**
4. [ ] Click **"Create Database"**
5. [ ] Wait 2-3 minutes ⏳
6. [ ] **SAVE THIS**: Copy the **Internal Database URL**
   ```
   Format: postgres://sdg_user:xxxxx@dpg-xxxxx-a/sdg_platform
   ```
7. [ ] **IMPORTANT**: Change `postgres://` to `postgresql://`
   ```
   Should be: postgresql://sdg_user:xxxxx@dpg-xxxxx-a/sdg_platform
   ```

**✅ Database Created!**

---

### STEP 2: Deploy Backend (10 minutes) 🐍

1. [ ] Click **"New +"** → **"Web Service"**
2. [ ] Choose **"Build and deploy from a Git repository"**
3. [ ] Click **"Next"**
4. [ ] Connect your GitHub account (if not already connected)
5. [ ] Select repository: `Anup1dubey/web_SDG`
6. [ ] Click **"Connect"**

#### Configure Backend:

7. [ ] **Name**: `sdg-platform-backend`
8. [ ] **Region**: (Same as database)
9. [ ] **Branch**: `main`
10. [ ] **Root Directory**: (Leave empty)
11. [ ] **Runtime**: **Python 3**
12. [ ] **Build Command**: 
    ```
    pip install -r backend/requirements.txt
    ```
13. [ ] **Start Command**: 
    ```
    cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
    ```
14. [ ] **Plan**: **Starter (Free)**

#### Add Environment Variables:

15. [ ] Click **"Advanced"** button
16. [ ] Click **"Add Environment Variable"**

**Variable 1 - DATABASE_URL:**
17. [ ] Key: `DATABASE_URL`
18. [ ] Value: (Paste the Internal Database URL from Step 1, starting with `postgresql://`)

**Variable 2 - SECRET_KEY:**
19. [ ] Key: `SECRET_KEY`
20. [ ] Value: Generate one by running on your computer:
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```
   Copy the output and paste it here.

**Variable 3 - CORS_ORIGINS:**
21. [ ] Key: `CORS_ORIGINS`
22. [ ] Value: `*`

23. [ ] Click **"Create Web Service"**
24. [ ] Wait 5-10 minutes for deployment ⏳
25. [ ] Watch the logs for completion

#### Verify Backend:

26. [ ] Once deployed, copy your backend URL:
    ```
    https://sdg-platform-backend.onrender.com
    ```
27. [ ] Visit: `https://sdg-platform-backend.onrender.com/docs`
28. [ ] **✅ You should see FastAPI documentation page!**

**✅ Backend Deployed!**

---

### STEP 3: Deploy Frontend (5 minutes) 🎨

1. [ ] Click **"New +"** → **"Static Site"**
2. [ ] Select the same repository: `Anup1dubey/web_SDG`
3. [ ] Click **"Connect"**

#### Configure Frontend:

4. [ ] **Name**: `sdg-platform-frontend`
5. [ ] **Branch**: `main`
6. [ ] **Root Directory**: (Leave empty)
7. [ ] **Build Command**: (Leave empty or type: `echo "No build"`)
8. [ ] **Publish Directory**: `frontend`

#### Optional - Add Environment Variable:

9. [ ] Click **"Advanced"**
10. [ ] Add environment variable:
    - **Key**: `API_URL`
    - **Value**: `https://sdg-platform-backend.onrender.com` (your backend URL)

11. [ ] Click **"Create Static Site"**
12. [ ] Wait 1-2 minutes ⏳

#### Verify Frontend:

13. [ ] Once deployed, copy your frontend URL:
    ```
    https://sdg-platform-frontend.onrender.com
    ```
14. [ ] Visit the URL in your browser
15. [ ] **✅ You should see the landing page!**

**✅ Frontend Deployed!**

---

### STEP 4: Update CORS Settings (Security) 🔒

1. [ ] Go back to your **backend service** in Render
2. [ ] Click **"Environment"** tab (left sidebar)
3. [ ] Find `CORS_ORIGINS` variable
4. [ ] Click **Edit** (pencil icon)
5. [ ] Change value from `*` to your frontend URL:
   ```
   https://sdg-platform-frontend.onrender.com
   ```
6. [ ] Click **"Save Changes"**
7. [ ] Backend will automatically redeploy (wait ~2 minutes)

**✅ CORS Configured!**

---

### STEP 5: Test Everything 🧪

#### Test Backend API:

1. [ ] Visit: `https://sdg-platform-backend.onrender.com/docs`
2. [ ] Try the `GET /api/health` endpoint
3. [ ] Should return: `{"status": "healthy"}`

#### Test Frontend:

4. [ ] Visit: `https://sdg-platform-frontend.onrender.com`
5. [ ] Open browser console (Press F12)
6. [ ] Look for: `API Base URL: https://sdg-platform-backend.onrender.com`
7. [ ] Click **"Register"** or **"Get Started"**
8. [ ] Create a test account
9. [ ] Log in with the test account
10. [ ] Navigate to Dashboard

#### Verify Database Connection:

11. [ ] Go to backend service in Render
12. [ ] Click **"Logs"** tab
13. [ ] Look for successful database connection messages

**✅ Everything Working!**

---

## 🎉 Deployment Complete!

### Your Live URLs:

- **Frontend**: `https://sdg-platform-frontend.onrender.com`
- **Backend**: `https://sdg-platform-backend.onrender.com`
- **API Docs**: `https://sdg-platform-backend.onrender.com/docs`

---

## 📋 Save These Details

| Service | Name | URL |
|---------|------|-----|
| Frontend | `sdg-platform-frontend` | `https://sdg-platform-frontend.onrender.com` |
| Backend | `sdg-platform-backend` | `https://sdg-platform-backend.onrender.com` |
| Database | `sdg-platform-db` | (Internal only) |

---

## ⚠️ Important Notes

### Free Tier Behavior:
- **Services sleep** after 15 minutes of inactivity
- **First request** takes 30-60 seconds (waking up)
- **This is normal** for free tier!

### Database Expiration:
- Free PostgreSQL database **expires after 90 days**
- You'll get email reminders before expiration
- Upgrade to paid ($7/month) to make it permanent

### Auto-Deploy:
- Every `git push` to `main` branch triggers auto-deploy
- Watch the logs to see deployment progress

---

## 🐛 Troubleshooting Quick Guide

### Backend shows error:
- [ ] Check logs: Backend service → Logs tab
- [ ] Verify `DATABASE_URL` is set correctly
- [ ] Make sure URL starts with `postgresql://` not `postgres://`

### Frontend blank page:
- [ ] Check browser console (F12) for errors
- [ ] Verify `Publish Directory` is `frontend`
- [ ] Check if files exist in GitHub repo

### CORS errors:
- [ ] Update backend `CORS_ORIGINS` to your frontend URL
- [ ] Make sure both services are deployed

### Can't create account:
- [ ] Check backend logs for errors
- [ ] Test backend `/docs` page directly
- [ ] Verify database connection in logs

---

## 📚 More Help

- **Full Manual Guide**: See `RENDER_MANUAL_SETUP.md`
- **Quick Start**: See `RENDER_QUICKSTART.md`
- **Render Docs**: https://render.com/docs
- **Community**: https://community.render.com

---

## 🚀 Next Steps

After deployment:

1. [ ] Test all features thoroughly
2. [ ] Share URLs with team/users
3. [ ] Monitor logs for issues
4. [ ] Set up custom domain (optional)
5. [ ] Plan for database upgrade before 90 days

---

**Congratulations! Your SDG Platform is live! 🌍✨**
