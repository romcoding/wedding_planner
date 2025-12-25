# Deployment Fix Guide

## Issues Found

### Vercel Issue
- **Problem**: Vercel can't find `wedding-planner-frontend` directory
- **Cause**: Configuration needs to be set in Vercel UI, not just vercel.json

### Render Issue  
- **Problem**: Start command not executing correctly
- **Cause**: Render might not be using render.yaml, or start command needs to be set in UI

## Solutions

### Fix 1: Vercel Configuration

**Option A: Configure in Vercel UI (Recommended)**

1. Go to your Vercel project settings
2. Navigate to **Settings** → **General**
3. Under **Root Directory**, set it to: `wedding-planner-frontend`
4. Save changes
5. Go to **Settings** → **Build & Development Settings**
6. Verify:
   - **Framework Preset**: Vite
   - **Build Command**: `pnpm run build` (or `npm run build`)
   - **Output Directory**: `dist`
   - **Install Command**: `pnpm install` (or `npm install`)
7. Redeploy

**Option B: Use Root vercel.json**

A `vercel.json` has been added to the root directory. This should work automatically.

### Fix 2: Render Configuration

**Update Start Command in Render UI:**

1. Go to Render Dashboard → Your Backend Service
2. Click **"Settings"** tab
3. Scroll to **"Start Command"**
4. Set it to:
   ```
   cd wedding-planner-backend && python src/main.py
   ```
5. **Also check "Build Command"** - should be:
   ```
   pip install -r wedding-planner-backend/requirements.txt
   ```
6. **Root Directory** should be: `.` (root of repo)
7. Click **"Save Changes"**
8. Render will automatically redeploy

**Alternative: If render.yaml isn't being used**

1. In Render, go to your service
2. Click **"Settings"**
3. Under **"Build & Deploy"**, make sure:
   - **Root Directory**: `.` (or leave empty)
   - **Build Command**: `pip install -r wedding-planner-backend/requirements.txt`
   - **Start Command**: `cd wedding-planner-backend && python src/main.py`

## Step-by-Step Fix

### Vercel Fix

1. **Go to Vercel Dashboard** → Your Project
2. **Settings** → **General**
3. **Root Directory**: Change to `wedding-planner-frontend`
4. **Save**
5. **Settings** → **Build & Development Settings**
6. Verify:
   - Build Command: `pnpm run build`
   - Output Directory: `dist`
   - Install Command: `pnpm install`
7. **Deployments** → **Redeploy** (or push a new commit)

### Render Fix

1. **Go to Render Dashboard** → Your Backend Service
2. **Settings** tab
3. **Build Command**: 
   ```
   pip install -r wedding-planner-backend/requirements.txt
   ```
4. **Start Command**:
   ```
   cd wedding-planner-backend && python src/main.py
   ```
5. **Root Directory**: `.` (or leave empty)
6. **Save Changes**
7. Wait for auto-redeploy

## Verification

After fixes:

### Vercel
- Check build logs - should show successful build
- Visit your Vercel URL - should see the app

### Render
- Check deployment logs - should show successful start
- Test: `https://your-backend.onrender.com/api/health`
- Should return: `{"status": "ok"}`

## If Still Having Issues

### Vercel Alternative Approach

If Root Directory doesn't work:

1. In Vercel, set **Root Directory** to: `.` (root)
2. Update **Build Command** to:
   ```
   cd wedding-planner-frontend && pnpm install && pnpm run build
   ```
3. Update **Output Directory** to:
   ```
   wedding-planner-frontend/dist
   ```

### Render Alternative Approach

If cd command doesn't work:

1. Set **Root Directory** to: `wedding-planner-backend`
2. Update **Start Command** to:
   ```
   python src/main.py
   ```
3. Update **Build Command** to:
   ```
   pip install -r requirements.txt
   ```

