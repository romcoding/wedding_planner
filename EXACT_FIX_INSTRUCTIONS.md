# 🔧 EXACT FIX INSTRUCTIONS - Follow These Steps

## Problem Analysis

### Issue 1: Vercel
- **Root Cause**: When Root Directory is set to `wedding-planner-frontend`, Vercel already changes to that directory. The commands `cd wedding-planner-frontend && pnpm install` try to cd into a directory that doesn't exist (we're already there).
- **Fix**: Remove `cd wedding-planner-frontend &&` from all commands. Just use `pnpm install` and `pnpm run build`.

### Issue 2: Render
- **Root Cause**: `psycopg2-binary==2.9.9` is incompatible with Python 3.13. The error `undefined symbol: _PyInterpreterState_Get` is a known compatibility issue.
- **Fix**: Pin Python version to 3.11 in Render.

## ✅ STEP-BY-STEP FIX

### Fix 1: Vercel (Do This First)

1. Go to **Vercel Dashboard** → Your Project (`wedding-planner`)
2. Click **"Settings"** → **"Build & Development Settings"**
3. **Update these three fields** (remove the `cd` part):

   **Install Command:**
   - ❌ Current (wrong): `cd wedding-planner-frontend && pnpm install`
   - ✅ Change to: `pnpm install`
   - Click the toggle to **ON** (blue)

   **Build Command:**
   - ❌ Current (wrong): `cd wedding-planner-frontend && pnpm run build` (or similar)
   - ✅ Change to: `pnpm run build`
   - Click the toggle to **ON** (blue)

   **Output Directory:**
   - ✅ Should be: `dist` (this is correct)
   - Click the toggle to **ON** (blue)

4. **Verify Root Directory** (Settings → General):
   - Should be: `wedding-planner-frontend` ✅
5. Click **"Save"**
6. Go to **"Deployments"** tab
7. Click **"Redeploy"** on the latest deployment

### Fix 2: Render (Do This Second)

1. Go to **Render Dashboard** → Your Backend Service
2. Click **"Settings"** tab
3. Scroll to **"Environment"** section
4. Click **"Add Environment Variable"**
5. Add this variable:
   - **Key**: `PYTHON_VERSION`
   - **Value**: `3.11.9`
   - Click **"Save"**
6. **Also verify these settings** (Settings → Build & Deploy):
   - **Root Directory**: `.` (or empty)
   - **Build Command**: `pip install -r wedding-planner-backend/requirements.txt`
   - **Start Command**: `cd wedding-planner-backend && PYTHONPATH=$(pwd):$PYTHONPATH python src/main.py`
7. Click **"Save Changes"**
8. Render will automatically redeploy (this will take longer as it rebuilds with Python 3.11)

## Why These Fixes Work

### Vercel
- When Root Directory = `wedding-planner-frontend`, Vercel's working directory is already `wedding-planner-frontend`
- Commands run from that directory, so no `cd` needed
- `pnpm install` and `pnpm run build` work directly

### Render
- Python 3.13 is too new - `psycopg2-binary` doesn't have compatible wheels yet
- Python 3.11.9 is stable and fully supported by all packages
- `PYTHON_VERSION` environment variable tells Render which Python to use
- The `runtime.txt` file I added also helps, but the env var is more reliable

## Verification

### After Vercel Fix:
- Build logs should show: `Running "install" command: pnpm install...`
- Should complete successfully
- No "No such file or directory" errors

### After Render Fix:
- Build logs should show Python 3.11 being used
- Should install packages successfully
- Should start Flask without import errors
- Test: `https://your-backend.onrender.com/api/health` should return `{"status": "ok"}`

## If Render Still Fails

If Python 3.11 doesn't work, try Python 3.12:

1. In Render Settings → Environment Variables
2. Change `PYTHON_VERSION` to: `3.12.7`
3. Save and redeploy

## Summary

**Vercel**: Remove `cd wedding-planner-frontend &&` from commands  
**Render**: Add `PYTHON_VERSION=3.11.9` environment variable

That's it! These two changes will fix both deployments.

