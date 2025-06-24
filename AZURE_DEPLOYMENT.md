# 🌍 CHIPFOLIO - Azure Deployment Guide

This guide will help you deploy your CHIPFOLIO poker tracker to Microsoft Azure using GitHub Actions.

## 📋 Prerequisites

- ✅ **Azure Account**: Free tier available at https://azure.microsoft.com/free/
- ✅ **GitHub Repository**: Your code is already on GitHub at https://github.com/atippa56/Chipfolio
- ✅ **Azure CLI** (optional): For command-line management

## 🚀 Step-by-Step Deployment

### Step 1: Create Azure Resources

#### 1.1 Create Azure Web App (Backend)
1. **Login to Azure Portal**: https://portal.azure.com
2. **Create a Resource** → **Web App**
3. **Configure**:
   - **Subscription**: Your Azure subscription
   - **Resource Group**: Create new → `chipfolio-resources`
   - **Name**: `chipfolio-backend` (must be globally unique)
   - **Runtime Stack**: `Python 3.9`
   - **Region**: Choose closest to your users
   - **Pricing Tier**: `Free F1` for testing, `Basic B1` for production

#### 1.2 Create Azure Static Web App (Frontend)
1. **Create a Resource** → **Static Web App**
2. **Configure**:
   - **Resource Group**: `chipfolio-resources` (same as above)
   - **Name**: `chipfolio-frontend`
   - **Region**: Same as backend
   - **Deployment Source**: `GitHub`
   - **GitHub Account**: Connect your GitHub account
   - **Repository**: `atippa56/Chipfolio`
   - **Branch**: `main`
   - **Build Presets**: `React`
   - **App Location**: `/frontend`
   - **Output Location**: `build`

### Step 2: Configure GitHub Secrets

Go to your GitHub repository → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

Add these secrets:

#### 2.1 Backend Secrets
- **`AZURE_WEBAPP_NAME`**: `chipfolio-backend` (your web app name)
- **`AZURE_WEBAPP_PUBLISH_PROFILE`**: 
  1. Go to Azure Portal → Your Web App → **Get publish profile**
  2. Download the `.publishsettings` file
  3. Copy the entire file content and paste as secret value

#### 2.2 Frontend Secrets
- **`AZURE_STATIC_WEB_APPS_API_TOKEN`**:
  1. Go to Azure Portal → Your Static Web App → **Manage deployment token**
  2. Copy the token and paste as secret value
- **`AZURE_BACKEND_URL`**: `https://chipfolio-backend.azurewebsites.net` (your backend URL)

### Step 3: Update Backend CORS Settings

The backend CORS is already configured for production. Just verify the Azure URL is allowed:

```python
# In backend/app/main.py - already configured
origins = [
    "http://localhost:3000",
    "https://your-static-web-app.azurestaticapps.net",  # Will be your actual URL
]
```

### Step 4: Deploy

#### 4.1 Automatic Deployment
- **Push to main branch** triggers automatic deployment
- **Check GitHub Actions** tab for deployment status
- **Monitor logs** for any issues

#### 4.2 Manual Deployment
If you need to redeploy:
```bash
git add .
git commit -m "Update for Azure deployment"
git push origin main
```

### Step 5: Configure Custom Domain (Optional)

#### 5.1 For Static Web App (Frontend)
1. **Azure Portal** → **Your Static Web App** → **Custom domains**
2. **Add custom domain** → Enter your domain
3. **Add DNS records** as instructed by Azure

#### 5.2 For Web App (Backend)
1. **Azure Portal** → **Your Web App** → **Custom domains**
2. **Add custom domain** → Enter your domain
3. **Configure DNS** with your domain provider

## 🔧 Environment Variables

### Backend Environment Variables
Set these in Azure Portal → Web App → **Configuration** → **Application settings**:

- `ENVIRONMENT`: `production`
- `DATABASE_URL`: Auto-configured for SQLite
- Add any other environment variables your app needs

### Frontend Environment Variables
These are set during build time via GitHub Actions:
- `REACT_APP_API_URL`: Automatically set to your backend URL

## 📊 Monitoring & Troubleshooting

### Application Insights (Recommended)
1. **Enable Application Insights** in both resources
2. **Monitor performance** and errors
3. **Set up alerts** for critical issues

### Log Monitoring
- **Web App Logs**: Azure Portal → Web App → **Log stream**
- **Static Web App Logs**: Check GitHub Actions logs
- **GitHub Actions**: Repository → **Actions** tab

### Common Issues

#### Backend Issues
- **Module not found**: Check `requirements.txt` includes all dependencies
- **Database errors**: Ensure SQLite database is properly initialized
- **CORS errors**: Verify frontend URL is in CORS origins

#### Frontend Issues
- **API connection**: Verify `REACT_APP_API_URL` points to correct backend
- **Build failures**: Check Node.js version compatibility
- **Static files**: Ensure build output is in correct directory

### Health Checks
- **Backend**: https://your-backend.azurewebsites.net/
- **Frontend**: https://your-frontend.azurestaticapps.net/
- **API Docs**: https://your-backend.azurewebsites.net/docs

## 💰 Cost Estimation

### Free Tier (Good for testing)
- **Web App**: Free F1 - $0/month (limited resources)
- **Static Web App**: Free tier - $0/month (100GB bandwidth)
- **Total**: **Free**

### Basic Production (Recommended)
- **Web App**: Basic B1 - ~$13/month
- **Static Web App**: Standard - ~$9/month (1TB bandwidth)
- **Total**: **~$22/month**

## 🔄 CI/CD Pipeline Features

Your GitHub Actions workflow includes:
- ✅ **Automated testing** (if tests exist)
- ✅ **Build optimization** for production
- ✅ **Parallel deployment** of frontend and backend
- ✅ **Error handling** and notifications
- ✅ **Rollback capability** via GitHub

## 🎯 Next Steps After Deployment

1. **Test all functionality** on the live site
2. **Set up monitoring** and alerts
3. **Configure backup** strategy
4. **Add SSL certificate** (auto-enabled on Azure)
5. **Monitor performance** and optimize as needed

## 🆘 Support Resources

- **Azure Documentation**: https://docs.microsoft.com/azure/
- **GitHub Actions**: https://docs.github.com/actions
- **Azure Support**: Available through Azure Portal
- **Community**: Stack Overflow, Azure Forums

---

Your CHIPFOLIO poker tracker will be live at:
- **Frontend**: `https://your-app.azurestaticapps.net`
- **Backend API**: `https://your-backend.azurewebsites.net`
- **API Docs**: `https://your-backend.azurewebsites.net/docs` 