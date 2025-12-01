# Deployment Guide: Free Hosting Options

## ⚠️ Important: Why Not GitHub Pages?

**GitHub Pages only hosts static websites** (HTML, CSS, JavaScript). Our project needs:
- ✅ Python backend (FastAPI)
- ✅ Database (SQLite/PostgreSQL)
- ✅ Server-side processing
- ✅ API endpoints

**Solution**: Use a free backend hosting service instead!

---

## 🎯 Recommended: Render.com (Best Free Option)

### Why Render?
- ✅ **Free tier**: 750 hours/month (enough for always-on service)
- ✅ **Automatic HTTPS**: Secure by default
- ✅ **Easy setup**: Connect GitHub, auto-deploy
- ✅ **PostgreSQL available**: Free database included
- ✅ **No credit card required**: Completely free
- ✅ **Backend support**: Perfect for FastAPI/Python apps

### Quick Setup (5 minutes):

1. **Push code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Create Render Account**
   - Go to https://render.com
   - Click "Get Started for Free"
   - Sign up with GitHub (one-click)

3. **Deploy Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select your repo
   - Configure:
     - **Name**: `carboncalc` (or your choice)
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt && python init_db.py`
     - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Click "Create Web Service"

4. **Wait for Deployment** (~5-10 minutes)
   - Watch the logs in Render dashboard
   - Your app will be live at: `https://carboncalc.onrender.com`

5. **Done!** 🎉
   - Your backend is now live and free
   - Access your API at the URL provided
   - Frontend can connect to this URL

### Render Configuration
Already included: `render.yaml` - Render can auto-detect these settings!

---

## 🚀 Alternative: Railway.app

### Why Railway?
- ✅ **$5 free credit monthly** (usually enough)
- ✅ **Simple deployment**
- ✅ **PostgreSQL included**
- ⚠️ Requires credit card (but won't charge on free tier)

### Steps:
1. Go to https://railway.app
2. Sign up with GitHub
3. "New Project" → "Deploy from GitHub repo"
4. Select repository
5. Railway auto-detects Python
6. Done! Get your URL

---

## 📊 Comparison Table

| Platform | Free Tier | Backend Support | Database | Credit Card | Best For |
|----------|-----------|-----------------|----------|-------------|----------|
| **Render.com** | ✅ 750 hrs/month | ✅ Yes | ✅ PostgreSQL | ❌ Not needed | **Recommended** |
| Railway.app | ✅ $5/month credit | ✅ Yes | ✅ PostgreSQL | ⚠️ Required | Advanced users |
| Fly.io | ✅ Generous | ✅ Yes | ⚠️ Manual | ❌ Not needed | CLI users |
| PythonAnywhere | ✅ Limited | ✅ Yes | ⚠️ MySQL only | ❌ Not needed | Simple apps |
| **GitHub Pages** | ✅ Unlimited | ❌ **No backend** | ❌ None | ❌ Not needed | **Static sites only** |

---

## 🖥️ Compute Requirements

### Good News: No GPU Needed!

Our ML models are **optimized for CPU** and run efficiently on:
- Standard servers (1-2 CPU cores)
- Free tier hosting (Render, Railway)
- Your local machine

**Model Complexity**:
- ✅ Uses scikit-learn (CPU-optimized)
- ✅ Lightweight ensemble models
- ✅ Fast training (< 5 seconds for typical datasets)
- ✅ Minimal memory (works with 512MB RAM)

**No GPU required** - models run on CPU using optimized algorithms!

---

## 🔧 Production Setup

### 1. Environment Variables

Set in Render/Railway dashboard:
```
SECRET_KEY=<generate-random-string>
DATABASE_URL=<auto-provided-or-set-manually>
API_HOST=0.0.0.0
API_PORT=$PORT
```

### 2. Database (Optional Upgrade)

For production, Render provides free PostgreSQL:
- Automatic backup
- Better performance
- More reliable

The code already supports both SQLite and PostgreSQL!

### 3. Custom Domain (Optional)

1. In Render dashboard → Settings → Custom Domains
2. Add your domain
3. Render provides SSL certificate automatically

---

## 📱 Frontend Deployment

Since the backend is on Render, deploy frontend separately:

### Option A: Keep Frontend with Backend
- Render serves both (current setup)
- Access at: `https://your-app.onrender.com`

### Option B: Deploy Frontend to GitHub Pages
- Build static frontend
- Deploy to GitHub Pages
- Connect to Render backend API
- Free frontend hosting!

### Option C: Netlify/Vercel (Free)
- Deploy frontend to Netlify
- Free tier available
- Connect to Render backend

---

## 🐛 Troubleshooting

### Build Fails?
- Check logs in Render dashboard
- Verify `requirements.txt` is correct
- Ensure Python version is compatible

### App Crashes?
- Check application logs
- Verify database initialization ran
- Check environment variables

### Slow Performance?
- First request may be slow (cold start)
- Render free tier has cold starts
- Consider upgrading for production (still cheap)

---

## 💰 Cost Breakdown

### Free Tier (Sufficient for Research Project):
- **Render.com**: $0/month (750 hours)
- **Railway**: $0/month ($5 credit, unused)
- **Total**: **FREE** ✅

### If You Need More:
- Render Pro: $7/month (always-on)
- Railway: Pay as you go
- Still very affordable!

---

## ✅ Recommended Setup for Your Project

1. **Backend**: Deploy to **Render.com** (free, easy)
2. **Frontend**: Serve from Render (included) OR deploy to GitHub Pages
3. **Database**: Use Render's free PostgreSQL (automatic)
4. **Domain**: Use Render's free subdomain or add custom domain

**Total Cost**: $0/month 🎉

---

## 📚 Step-by-Step Tutorial

### Render.com Deployment:

1. **GitHub Setup**:
   ```bash
   # In your project folder
   git init
   git add .
   git commit -m "Ready for deployment"
   # Push to GitHub (create repo first on GitHub.com)
   git remote add origin https://github.com/yourusername/carboncalc.git
   git push -u origin main
   ```

2. **Render Setup**:
   - Visit https://render.com
   - Sign up with GitHub
   - Click "New +" → "Web Service"
   - Select repository
   - Use these settings:
     ```
     Name: carboncalc
     Build Command: pip install -r requirements.txt && python init_db.py
     Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
     ```
   - Click "Create Web Service"

3. **Wait & Deploy**:
   - Render will build and deploy automatically
   - Check logs if issues occur
   - Get your URL (e.g., `https://carboncalc.onrender.com`)

4. **Test**:
   - Visit your URL
   - Test API: `https://your-app.onrender.com/health`
   - Should return: `{"status": "healthy"}`

**Done!** Your research project is now live! 🚀

---

## 📞 Need Help?

- Render Docs: https://render.com/docs
- Railway Docs: https://docs.railway.app
- Project Issues: Check GitHub issues

---

*Last Updated: 2024*
*Recommended Platform: Render.com for easiest free deployment*
