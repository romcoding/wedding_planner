# 🚨 URGENT: Fix Deployment Issues

## Problem Summary

1. **Render**: Python can't find `src` module (import path issue)
2. **Vercel**: Can't find `wedding-planner-frontend` directory

## ✅ IMMEDIATE FIXES

### Fix 1: Render - Update Start Command in UI

**The render.yaml might not be used. You MUST update in Render UI:**

1. Go to **Render Dashboard** → Your Backend Service
2. Click **"Settings"** tab
3. Scroll to **"Start Command"**
4. **REPLACE** the current command with:
   ```
   cd wedding-planner-backend && PYTHONPATH=$(pwd):$PYTHONPATH python src/main.py
   ```
5. **Also verify "Build Command"** is:
   ```
   pip install -r wedding-planner-backend/requirements.txt
   ```
6. **Root Directory** should be: `.` (or leave empty)
7. Click **"Save Changes"**
8. Wait for auto-redeploy

### Fix 2: Vercel - Set Root Directory in UI

**Vercel MUST be configured in the UI, not just vercel.json:**

1. Go to **Vercel Dashboard** → Your Project
2. Click **"Settings"** → **"General"**
3. Scroll to **"Root Directory"**
4. **Set it to**: `wedding-planner-frontend`
5. Click **"Save"**
6. Go to **"Settings"** → **"Build & Development Settings"**
7. Verify these are set (should auto-populate after setting root):
   - **Build Command**: `pnpm run build`
   - **Output Directory**: `dist`
   - **Install Command**: `pnpm install`
8. Go to **"Deployments"** tab
9. Click **"Redeploy"** on the latest deployment

## Alternative Render Fix (If Above Doesn't Work)

If the PYTHONPATH approach doesn't work, try this:

1. In Render Settings → **"Start Command"**, use:
   ```
   cd /opt/render/project/src/wedding-planner-backend && python -m src.main
   ```
   
   OR set **Root Directory** to `wedding-planner-backend` and use:
   ```
   python src/main.py
   ```

## Verification

After fixes:

### Render
- Check logs - should see Flask starting
- Test: `https://your-backend.onrender.com/api/health`
- Should return: `{"status": "ok"}`

### Vercel  
- Check build logs - should complete successfully
- Visit your Vercel URL - should see the app

## Why This Happened

- **Render**: Python import paths are relative to where Python is executed. When `cd wedding-planner-backend`, Python can't find `src` because it's not in the Python path.
- **Vercel**: The root directory wasn't set in the UI, so Vercel was looking in the wrong place.

## Next Steps After Fix

1. ✅ Both services should deploy successfully
2. ✅ Update `FRONTEND_URL` in Render to your Vercel URL
3. ✅ Create admin user via Render Shell
4. ✅ Test the application

