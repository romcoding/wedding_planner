# Vercel Frontend Setup - Step by Step Guide

## Prerequisites

✅ Your backend is deployed on Render  
✅ You have your Render backend URL (e.g., `https://wedding-planner-backend.onrender.com`)

## Step 1: Navigate to Vercel

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Sign in with your GitHub account (recommended) or email

## Step 2: Import Your Project

1. Click **"Add New..."** button in the top right
2. Select **"Project"** from the dropdown
3. You'll see your GitHub repositories
4. **Find and select** your `wedding-planner` repository
5. Click **"Import"**

## Step 3: Configure Project Settings

Vercel will auto-detect some settings, but verify/update these:

### Framework Preset
- **Framework Preset**: Should auto-detect as **"Vite"** ✅
- If not, manually select **"Vite"**

### Root Directory
- Click **"Edit"** next to Root Directory
- Change from `./` to: `wedding-planner-frontend`
- This tells Vercel where your frontend code is

### Build and Output Settings
- **Build Command**: Should be `pnpm run build` (or `npm run build`)
- **Output Directory**: Should be `dist`
- **Install Command**: Should be `pnpm install` (or `npm install`)

### These should be auto-detected, but verify:
- ✅ Framework: Vite
- ✅ Root Directory: `wedding-planner-frontend`
- ✅ Build Command: `pnpm run build`
- ✅ Output Directory: `dist`

## Step 4: Add Environment Variables

Click **"Environment Variables"** section to expand it.

### Add VITE_API_URL

1. Click **"Add"** or the **"+"** button
2. **Key**: `VITE_API_URL`
3. **Value**: Your Render backend URL + `/api`
   - Example: `https://wedding-planner-backend.onrender.com/api`
   - ⚠️ **Important**: Include `/api` at the end!
4. **Environment**: Select all three:
   - ✅ Production
   - ✅ Preview
   - ✅ Development
5. Click **"Save"**

## Step 5: Deploy

1. Review all settings one more time
2. Click **"Deploy"** button at the bottom
3. Vercel will start building your project

## Step 6: Monitor the Build

1. You'll see build logs in real-time
2. Wait for the build to complete (usually 1-3 minutes)
3. Look for:
   - ✅ "Build successful"
   - ✅ "Deployment ready"
   - ⚠️ Any errors (check the logs)

## Step 7: Get Your Deployment URL

Once deployed, you'll see:
- **Production URL**: `https://wedding-planner.vercel.app` (or similar)
- **Deployment Status**: ✅ Ready

**Save this URL!** You'll need it for the next step.

## Step 8: Update Render Backend CORS

Now we need to tell your backend to accept requests from Vercel:

1. Go back to your **Render Dashboard**
2. Navigate to your backend web service
3. Click on **"Environment"** tab
4. Find `FRONTEND_URL` variable
5. Click the **edit icon** (pencil icon)
6. Update the value to your **Vercel URL**:
   - Example: `https://wedding-planner.vercel.app`
   - ⚠️ **Important**: 
     - Use `https://` (not `http://`)
     - No trailing slash
     - No `/api` at the end
7. Click **"Save"**
8. Render will automatically redeploy (this takes 1-2 minutes)

## Step 9: Test Your Deployment

### Test Frontend
1. Visit your Vercel URL: `https://your-app.vercel.app`
2. You should see the guest registration page
3. Try accessing: `https://your-app.vercel.app/admin/login`
4. You should see the admin login page

### Test Backend Connection
1. Open browser DevTools (F12)
2. Go to Network tab
3. Visit your frontend
4. Check if API calls are working (they should go to your Render backend)

## Step 10: Create Admin User (If Not Done Yet)

If you haven't created an admin user yet:

### Option A: Using Render Shell
1. Go to Render dashboard → Your backend service
2. Click **"Shell"** tab
3. Run:
   ```bash
   cd wedding-planner-backend
   python create_admin.py
   ```

### Option B: Using API
```bash
curl -X POST https://your-backend-url.onrender.com/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "your-password",
    "name": "Admin User"
  }'
```

## Step 11: Login and Test

1. Go to: `https://your-vercel-url.vercel.app/admin/login`
2. Login with your admin credentials
3. You should see the admin dashboard
4. Test features:
   - View dashboard analytics
   - Add content for guests
   - Test guest registration on the home page

## Troubleshooting

### Build Fails
- Check build logs for errors
- Verify `package.json` is correct
- Ensure Node.js version is 18+

### API Connection Errors
- Verify `VITE_API_URL` is correct (includes `/api`)
- Check browser console for CORS errors
- Verify `FRONTEND_URL` in Render matches Vercel URL exactly

### 404 Errors on Routes
- This is normal for SPAs - Vercel handles this automatically
- If issues persist, check `vercel.json` configuration

### CORS Errors
- Double-check `FRONTEND_URL` in Render matches Vercel URL exactly
- No trailing slashes
- Use `https://` not `http://`
- Wait for Render to redeploy after updating

## Your URLs

Save these for reference:

**Frontend (Vercel):**
```
https://your-app.vercel.app
```

**Backend (Render):**
```
https://your-backend.onrender.com
```

**API Endpoint:**
```
https://your-backend.onrender.com/api
```

## Next Steps

✅ Frontend is deployed!  
✅ Backend is configured!  
✅ You're ready to use your wedding planner app!

### What to Do Next:
1. ✅ Login to admin dashboard
2. ✅ Add wedding content (Content Management page)
3. ✅ Test guest registration
4. ✅ Start planning your wedding! 🎉

## Custom Domain (Optional)

Both Vercel and Render support custom domains:
- **Vercel**: Go to Project Settings → Domains
- **Render**: Go to Service Settings → Custom Domains

