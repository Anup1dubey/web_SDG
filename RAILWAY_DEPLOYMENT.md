# 🚂 Deploying Backend on Railway (Recommended)

Railway is perfect for hosting your FastAPI backend with persistent database support.

## Why Railway?

✅ **Free Tier** - $5 monthly credit (enough for small projects)
✅ **Persistent Storage** - Database survives between requests
✅ **Auto-deployment** - Push to GitHub and it deploys automatically
✅ **Easy Setup** - No configuration needed

---

## 🚀 Step-by-Step Deployment

### 1. Prepare Your Repository

First, push your code to GitHub if you haven't already:

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/your-username/your-repo.git
git push -u origin main
```

### 2. Sign Up for Railway

1. Go to [Railway.app](https://railway.app)
2. Click "Login" and sign in with GitHub
3. Authorize Railway to access your repositories

### 3. Create New Project

1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your SDG Digital Twin repository
4. Railway will detect it's a Python project

### 4. Configure the Backend

1. In the Railway dashboard, click on your project
2. Go to "Settings"
3. Set **Root Directory** to: `backend`
4. Set **Start Command** to: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### 5. Add Environment Variables (Optional)

1. Go to "Variables" tab
2. Add any environment variables you need:
   ```
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=sqlite:///./sdg_platform.db
   ```

### 6. Deploy!

Railway will automatically:
- ✅ Install dependencies from `requirements.txt`
- ✅ Start your FastAPI server
- ✅ Generate a public URL

Your backend will be available at: `https://your-app.railway.app`

### 7. Get Your Backend URL

1. Click on your project in Railway dashboard
2. Go to "Settings" → "Domains"
3. Copy the generated domain (e.g., `https://your-app-production.up.railway.app`)

---

## 🔗 Connect Frontend to Backend

### Update `frontend/auth.js`

Change the API base URL:

```javascript
// Old (local development)
const API_BASE = 'http://localhost:8000';

// New (production)
const API_BASE = 'https://your-app-production.up.railway.app';
```

### Update CORS in `backend/main.py`

Add your frontend domain:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-vercel-app.vercel.app",  # Your Vercel frontend URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📋 Deploy Frontend to Vercel

Now deploy your frontend to Vercel:

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
vercel
```

---

## ✅ Complete Deployment Checklist

- [ ] Push code to GitHub
- [ ] Sign up for Railway
- [ ] Create new project from GitHub repo
- [ ] Set root directory to `backend`
- [ ] Set start command to `uvicorn main:app --host 0.0.0.0 --port $PORT`
- [ ] Get Railway backend URL
- [ ] Update `API_BASE` in `frontend/auth.js`
- [ ] Update CORS in `backend/main.py`
- [ ] Push changes to GitHub (Railway auto-deploys)
- [ ] Deploy frontend to Vercel
- [ ] Test the complete application

---

## 🔄 Automatic Deployments

Railway automatically deploys when you push to GitHub:

```bash
# Make changes
git add .
git commit -m "Update feature"
git push

# Railway automatically detects and deploys! 🎉
```

---

## 📊 Monitoring

### View Logs

1. Go to Railway dashboard
2. Click on your project
3. Go to "Deployments" tab
4. Click on any deployment to see logs

### Check Database

Railway provides a built-in file browser:
1. Go to "Data" tab
2. You can view your SQLite database file

---

## 💰 Pricing

**Free Tier:**
- $5 of usage per month
- Usually enough for:
  - Small projects
  - Demos
  - Personal use
  - Development/staging environments

**Pro Tier ($20/month):**
- $20 credit included
- Pay only for what you use beyond that

---

## 🐛 Troubleshooting

### Issue: Port binding error
**Solution:** Make sure start command uses `$PORT` variable:
```
uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Issue: Module not found
**Solution:** Ensure `requirements.txt` is in the backend directory

### Issue: CORS errors
**Solution:** Add your Vercel domain to CORS allowed origins

---

## 🎉 You're Done!

Your application is now live:
- **Backend:** `https://your-app.railway.app`
- **Frontend:** `https://your-app.vercel.app`

### Next Steps:
1. Test all features
2. Set up custom domains (optional)
3. Monitor usage in Railway dashboard
4. Share your deployed app! 🌍

---

## 📚 Additional Resources

- [Railway Documentation](https://docs.railway.app)
- [Railway Python Guide](https://docs.railway.app/guides/python)
- [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/)
