# 🚀 Deploying SDG Digital Twin Platform on Vercel

## ⚠️ Important Considerations

### What Works on Vercel:
✅ **Frontend** - All HTML, CSS, and JavaScript files will be served as static assets
✅ **API Endpoints** - FastAPI backend will run as serverless functions

### Limitations:
⚠️ **SQLite Database** - Vercel's serverless functions are stateless, so SQLite won't persist data between requests
⚠️ **File Storage** - The filesystem is read-only (except `/tmp`)

### Recommended Solution:
For production deployment on Vercel, you should:
1. Use a cloud database (PostgreSQL, MongoDB, etc.)
2. Or deploy the backend on a different service (Railway, Render, Heroku)

---

## Option 1: Deploy Frontend Only (Recommended for Demo)

This deploys only the frontend, and you'll need to update the API base URL to point to your backend hosted elsewhere.

### Steps:

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Create `.vercelignore` file**
   Add this file to exclude backend:
   ```
   backend/
   *.bat
   *.md
   .gitignore
   ```

4. **Create `vercel.json` for frontend only**
   ```json
   {
     "version": 2,
     "builds": [
       {
         "src": "frontend/**",
         "use": "@vercel/static"
       }
     ],
     "routes": [
       {
         "src": "/(.*\\.(js|css|html|png|jpg|jpeg|gif|svg|ico))",
         "dest": "/frontend/$1"
       },
       {
         "src": "/",
         "dest": "/frontend/landing.html"
       },
       {
         "src": "/(.*)",
         "dest": "/frontend/$1"
       }
     ]
   }
   ```

5. **Update API Base URL in `frontend/auth.js`**
   Change:
   ```javascript
   const API_BASE = 'http://localhost:8000';
   ```
   To your deployed backend URL:
   ```javascript
   const API_BASE = 'https://your-backend-url.com';
   ```

6. **Deploy**
   ```bash
   vercel
   ```

---

## Option 2: Full Stack Deployment (With Limitations)

⚠️ **Warning:** This will work but data won't persist between requests due to SQLite limitations.

### Steps:

1. **The `vercel.json` is already configured in the root directory**

2. **Deploy**
   ```bash
   vercel
   ```

3. **Set Environment Variables** (if needed)
   ```bash
   vercel env add SECRET_KEY
   ```

---

## Option 3: Hybrid Deployment (Best for Production)

### Frontend: Vercel
### Backend: Railway/Render/Heroku

1. **Deploy Backend to Railway**
   - Go to [Railway.app](https://railway.app)
   - Click "Start a New Project"
   - Select "Deploy from GitHub repo"
   - Connect your repository
   - Set root directory to `backend`
   - Railway will auto-detect Python and install dependencies
   - Add environment variables if needed
   - Get your backend URL (e.g., `https://your-app.railway.app`)

2. **Deploy Frontend to Vercel**
   - Follow "Option 1" above
   - Update `API_BASE` in `frontend/auth.js` to your Railway backend URL

---

## 🔧 Post-Deployment Configuration

### Update CORS Settings

In your `backend/main.py`, update CORS origins:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-vercel-app.vercel.app",  # Add your Vercel URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Update API Base URL

In `frontend/auth.js`:
```javascript
const API_BASE = 'https://your-backend-url.com';  // Update this
```

---

## 📝 Quick Deployment Checklist

- [ ] Install Vercel CLI: `npm install -g vercel`
- [ ] Login: `vercel login`
- [ ] Choose deployment option (1, 2, or 3)
- [ ] Update API base URL in frontend
- [ ] Update CORS settings in backend
- [ ] Deploy: `vercel`
- [ ] Test the deployment
- [ ] Set up custom domain (optional)

---

## 🌐 Setting Up Custom Domain

1. Go to your Vercel dashboard
2. Select your project
3. Go to "Settings" → "Domains"
4. Add your custom domain
5. Follow DNS configuration instructions

---

## 🐛 Troubleshooting

### Issue: API calls fail with CORS error
**Solution:** Make sure your backend CORS settings include your Vercel domain

### Issue: Database not persisting
**Solution:** Use a cloud database like PostgreSQL (Neon, Supabase) or MongoDB Atlas

### Issue: 500 Internal Server Error
**Solution:** Check Vercel logs: `vercel logs`

---

## 📚 Additional Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Railway Documentation](https://docs.railway.app)
- [Deploying FastAPI on Vercel](https://vercel.com/guides/deploying-fastapi-with-vercel)

---

## 💡 Recommended: Use Railway for Backend

For the best experience, I recommend:

1. **Backend** → Deploy to Railway (free tier available, persistent database)
2. **Frontend** → Deploy to Vercel (free tier, excellent performance)

This gives you:
- ✅ Persistent database
- ✅ Fast frontend delivery
- ✅ Separate scaling
- ✅ Both have generous free tiers

Would you like detailed instructions for Railway deployment?
