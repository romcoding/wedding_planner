# Render Backend Setup - Step by Step Guide

Since you've already created the PostgreSQL database `wedding-planner-db`, let's set up the web service.

## Step 1: Navigate to Render Dashboard

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Make sure you're logged in

## Step 2: Create New Web Service

1. Click the **"New +"** button in the top right
2. Select **"Web Service"** from the dropdown

## Step 3: Connect Your GitHub Repository

1. You'll see options to connect a repository:
   - If this is your first time, click **"Connect GitHub"** and authorize Render
   - If you've connected before, you'll see your repositories
2. **Search for and select** your `wedding-planner` repository
3. Click **"Connect"**

## Step 4: Configure the Web Service

Fill in the following settings:

### Basic Settings
- **Name**: `wedding-planner-backend` (or your preferred name)
- **Region**: Choose the region closest to you (or your users)
- **Branch**: `main` (or `master` if that's your default branch)
- **Root Directory**: Leave **empty** (the root of the repo is fine)

### Build & Deploy Settings
- **Environment**: Select **"Python 3"**
- **Build Command**: 
  ```
  pip install -r wedding-planner-backend/requirements.txt
  ```
- **Start Command**: 
  ```
  cd wedding-planner-backend && python src/main.py
  ```

### Advanced Settings (Click to expand)
- **Auto-Deploy**: Keep it as **"Yes"** (deploys automatically on git push)
- **Health Check Path**: Leave empty (or use `/api/health`)

## Step 5: Add Environment Variables

Click **"Add Environment Variable"** and add each of these:

### 1. DATABASE_URL
- **Key**: `DATABASE_URL`
- **Value**: Get this from your PostgreSQL database:
  1. Go to your database `wedding-planner-db` in Render
  2. Find the **"Internal Database URL"** section
  3. Copy the **Internal Database URL** (starts with `postgresql://`)
  4. Paste it as the value
- **Important**: Use the **Internal Database URL**, not the External one (faster and more secure)

### 2. SECRET_KEY
- **Key**: `SECRET_KEY`
- **Value**: Generate a random secret key. You can use:
  ```bash
  python -c "import secrets; print(secrets.token_urlsafe(32))"
  ```
  Or use any long random string (at least 32 characters)

### 3. JWT_SECRET_KEY
- **Key**: `JWT_SECRET_KEY`
- **Value**: Generate another random secret key (different from SECRET_KEY)
  ```bash
  python -c "import secrets; print(secrets.token_urlsafe(32))"
  ```

### 4. FRONTEND_URL
- **Key**: `FRONTEND_URL`
- **Value**: We'll set this after deploying to Vercel. For now, use:
  ```
  http://localhost:5173
  ```
  **⚠️ Important**: You'll need to update this after Vercel deployment with your actual Vercel URL

### 5. PORT
- **Key**: `PORT`
- **Value**: `10000`
- **Note**: Render automatically sets this, but it's good to be explicit

## Step 6: Create the Web Service

1. Review all your settings
2. Scroll down and click **"Create Web Service"**
3. Render will start building and deploying your application

## Step 7: Monitor the Deployment

1. You'll see the build logs in real-time
2. Wait for the build to complete (usually 2-5 minutes)
3. Look for:
   - ✅ "Build successful"
   - ✅ "Your service is live at https://wedding-planner-backend.onrender.com"
   - ⚠️ Any errors (check the logs)

## Step 8: Test the Deployment

1. Once deployed, you'll see your service URL (e.g., `https://wedding-planner-backend.onrender.com`)
2. Test the health endpoint:
   - Visit: `https://your-service-url.onrender.com/api/health`
   - You should see: `{"status": "ok"}`

## Step 9: Create Your First Admin User

After deployment, create an admin user. You have two options:

### Option A: Using Render Shell (Recommended)

1. In your Render dashboard, go to your web service
2. Click on **"Shell"** tab
3. Run:
   ```bash
   cd wedding-planner-backend
   python create_admin.py
   ```
4. Follow the prompts to create your admin user

### Option B: Using API (Alternative)

Use curl or Postman:
```bash
curl -X POST https://your-service-url.onrender.com/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "your-secure-password",
    "name": "Admin User"
  }'
```

## Step 10: Update FRONTEND_URL (After Vercel Deployment)

Once you've deployed to Vercel (see Vercel setup guide):

1. Go back to your Render web service
2. Click **"Environment"** tab
3. Find `FRONTEND_URL`
4. Click the edit icon
5. Update to your Vercel URL: `https://your-app.vercel.app`
6. Save changes
7. Render will automatically redeploy

## Troubleshooting

### Build Fails
- Check build logs for errors
- Verify `requirements.txt` is correct
- Ensure Python 3.11+ is available

### Database Connection Errors
- Verify `DATABASE_URL` uses Internal Database URL
- Check database is running
- Ensure database name matches

### Service Won't Start
- Check start command is correct
- Verify `main.py` exists in the right location
- Check logs for Python errors

### CORS Errors (After Frontend Deployment)
- Make sure `FRONTEND_URL` matches your Vercel URL exactly
- No trailing slashes
- Include `https://`

## Next Steps

✅ Backend is deployed!  
➡️ Now proceed to **Vercel Frontend Setup**

## Your Backend URL

Save this URL - you'll need it for Vercel:
```
https://your-service-name.onrender.com
```

