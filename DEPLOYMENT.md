# Deployment Guide

This guide explains how to deploy the Wedding Planner application to Render (backend) and Vercel (frontend).

## Prerequisites

- GitHub account
- Render account (for backend)
- Vercel account (for frontend)
- PostgreSQL database (Render provides this)

## Backend Deployment (Render)

### Step 1: Create PostgreSQL Database

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New +" → "PostgreSQL"
3. Configure:
   - Name: `wedding-planner-db`
   - Database: `wedding_planner`
   - User: (auto-generated)
   - Region: Choose closest to you
4. Click "Create Database"
5. Copy the **Internal Database URL** (you'll need this)

### Step 2: Deploy Backend Service

1. In Render Dashboard, click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure the service:
   - **Name**: `wedding-planner-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r wedding-planner-backend/requirements.txt`
   - **Start Command**: `cd wedding-planner-backend && python src/main.py`
   - **Root Directory**: Leave empty (or set to repository root)

4. Add Environment Variables:
   ```
   DATABASE_URL=<your-postgres-internal-url>
   SECRET_KEY=<generate-a-random-secret-key>
   JWT_SECRET_KEY=<generate-another-random-secret-key>
   FRONTEND_URL=https://your-frontend-url.vercel.app
   PORT=10000
   ```

5. Click "Create Web Service"
6. Wait for deployment to complete
7. Copy the service URL (e.g., `https://wedding-planner-backend.onrender.com`)

### Step 3: Update Database URL Format

If your Render PostgreSQL URL starts with `postgres://`, you may need to update it to `postgresql://` in the environment variables. The code handles this automatically, but verify it works.

## Frontend Deployment (Vercel)

### Step 1: Deploy to Vercel

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "Add New..." → "Project"
3. Import your GitHub repository
4. Configure the project:
   - **Framework Preset**: Vite
   - **Root Directory**: `wedding-planner-frontend`
   - **Build Command**: `pnpm run build` (or `npm run build`)
   - **Output Directory**: `dist`
   - **Install Command**: `pnpm install` (or `npm install`)

5. Add Environment Variables:
   ```
   VITE_API_URL=https://your-backend-url.onrender.com/api
   ```

6. Click "Deploy"
7. Wait for deployment to complete
8. Copy the deployment URL (e.g., `https://wedding-planner.vercel.app`)

### Step 2: Update Backend CORS

1. Go back to Render dashboard
2. Edit your backend service
3. Update the `FRONTEND_URL` environment variable to your Vercel URL:
   ```
   FRONTEND_URL=https://your-frontend-url.vercel.app
   ```
4. Save and redeploy

## Post-Deployment Setup

### Create Admin User

After deployment, you'll need to create an admin user. You can do this by:

1. **Option 1: Using the API directly**
   ```bash
   curl -X POST https://your-backend-url.onrender.com/api/auth/register \
     -H "Content-Type: application/json" \
     -d '{
       "email": "admin@example.com",
       "password": "your-secure-password",
       "name": "Admin User"
     }'
   ```

2. **Option 2: Add a script** (recommended for production)
   Create a script in the backend to initialize an admin user on first deployment.

### Initialize Content

You may want to add initial content for the guest portal. Use the admin dashboard or API to add content items like:
- Welcome message
- Venue information
- Schedule
- FAQs

## Troubleshooting

### Backend Issues

- **Database Connection**: Ensure `DATABASE_URL` uses the internal database URL from Render
- **CORS Errors**: Verify `FRONTEND_URL` matches your Vercel deployment URL exactly
- **Port Issues**: Render uses port 10000 by default, ensure `PORT=10000` is set

### Frontend Issues

- **API Connection**: Verify `VITE_API_URL` points to your Render backend URL with `/api` suffix
- **Build Errors**: Check that all dependencies are in `package.json`
- **Routing Issues**: Vercel should handle SPA routing automatically with the `vercel.json` configuration

## Environment Variables Summary

### Backend (Render)
- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - Flask secret key
- `JWT_SECRET_KEY` - JWT signing key
- `FRONTEND_URL` - Vercel deployment URL
- `PORT` - Port number (10000 for Render)

### Frontend (Vercel)
- `VITE_API_URL` - Backend API URL (with `/api` suffix)

## Custom Domains

Both Render and Vercel support custom domains. Configure them in their respective dashboards after initial deployment.

## Monitoring

- **Render**: Check logs in the Render dashboard
- **Vercel**: Check logs in the Vercel dashboard
- **Database**: Monitor in Render PostgreSQL dashboard

## Security Notes

- Never commit `.env` files
- Use strong, randomly generated secrets
- Keep database URLs private
- Regularly update dependencies
- Use HTTPS (enabled by default on both platforms)

