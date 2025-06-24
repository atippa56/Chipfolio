# 🚀 CHIPFOLIO - Quick Deployment Guide

## Prerequisites
- GitHub account
- Vercel account (free): https://vercel.com
- Railway account (free): https://railway.app

## Step 1: Prepare Your Code

1. **Git Setup** (run in Bankroll directory):
```bash
git init
git add .
git commit -m "Initial commit - CHIPFOLIO poker tracker with equity calculator"
```

2. **Push to GitHub**:
   - Create a new repository at https://github.com/new
   - Name it "chipfolio" or "poker-bankroll-tracker"
   - Run these commands:
```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

## Step 2: Deploy Backend to Railway

1. **Go to Railway**: https://railway.app
2. **Login/Signup** with GitHub
3. **Create New Project** → "Deploy from GitHub repo"
4. **Select your repository**
5. **Configure**:
   - Root Directory: `backend`
   - Build Command: (automatic)
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. **Add Environment Variables**:
   - `PYTHONPATH` = `/app`
   - `DATABASE_URL` = `sqlite:///./bankroll.db`
7. **Deploy** - Railway will give you a URL like `https://your-app.railway.app`

## Step 3: Deploy Frontend to Vercel

1. **Go to Vercel**: https://vercel.com
2. **Login/Signup** with GitHub
3. **Import Project** → Select your repository
4. **Configure**:
   - Framework Preset: "Create React App"
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `build`
5. **Environment Variables**:
   - `REACT_APP_API_URL` = `https://your-railway-url.railway.app`
6. **Deploy** - Vercel will give you a URL like `https://your-app.vercel.app`

## Step 4: Update API URL

1. **Edit** `frontend/src/services/api.ts`
2. **Replace** the localhost URL with your Railway URL:
```typescript
const API_BASE_URL = 'https://your-railway-url.railway.app';
```
3. **Commit and push**:
```bash
git add .
git commit -m "Update API URL for production"
git push
```

## Step 5: Test Your Live App!

Visit your Vercel URL and enjoy your live CHIPFOLIO app! 🎉

### Troubleshooting
- **CORS Issues**: Railway might need CORS configuration
- **Database**: SQLite file will persist on Railway
- **Logs**: Check Railway logs for backend issues
- **Build Errors**: Check Vercel build logs

### Post-Deployment Edits
- **Code Changes**: Push to GitHub → Auto-redeploys
- **Database**: Access via Railway dashboard
- **Domains**: Add custom domain in Vercel/Railway settings 