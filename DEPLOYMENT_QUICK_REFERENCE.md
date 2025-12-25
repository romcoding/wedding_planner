# Deployment Quick Reference

## 🚀 Quick Deployment Checklist

### ✅ Step 1: Push to GitHub
```bash
# Create repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/wedding-planner.git
git branch -M main
git push -u origin main
```

### ✅ Step 2: Render Backend Setup

1. **Create Web Service** in Render Dashboard
2. **Connect GitHub** repository
3. **Configure**:
   - Name: `wedding-planner-backend`
   - Environment: Python 3
   - Build: `pip install -r wedding-planner-backend/requirements.txt`
   - Start: `cd wedding-planner-backend && python src/main.py`
4. **Add Environment Variables**:
   - `DATABASE_URL` = Internal Database URL from your PostgreSQL database
   - `SECRET_KEY` = Random secret (32+ chars)
   - `JWT_SECRET_KEY` = Random secret (32+ chars)
   - `FRONTEND_URL` = `http://localhost:5173` (update after Vercel)
   - `PORT` = `10000`
5. **Deploy** and wait for completion
6. **Create Admin User** via Render Shell:
   ```bash
   cd wedding-planner-backend
   python create_admin.py
   ```

### ✅ Step 3: Vercel Frontend Setup

1. **Import Project** from GitHub in Vercel
2. **Configure**:
   - Root Directory: `wedding-planner-frontend`
   - Framework: Vite (auto-detected)
   - Build: `pnpm run build`
   - Output: `dist`
3. **Add Environment Variable**:
   - `VITE_API_URL` = `https://your-backend.onrender.com/api`
4. **Deploy** and wait for completion
5. **Save Vercel URL**

### ✅ Step 4: Connect Frontend to Backend

1. Go to Render → Your Backend Service → Environment
2. Update `FRONTEND_URL` to your Vercel URL
3. Wait for auto-redeploy

## 🔑 Key URLs to Save

- **Backend**: `https://your-backend.onrender.com`
- **Frontend**: `https://your-app.vercel.app`
- **API**: `https://your-backend.onrender.com/api`

## 📝 Environment Variables Summary

### Render (Backend)
```
DATABASE_URL=postgresql://... (Internal URL)
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
FRONTEND_URL=https://your-app.vercel.app
PORT=10000
```

### Vercel (Frontend)
```
VITE_API_URL=https://your-backend.onrender.com/api
```

## 🆘 Quick Troubleshooting

**Build fails?** → Check logs, verify paths
**CORS errors?** → Verify FRONTEND_URL matches Vercel URL exactly
**Database errors?** → Use Internal Database URL, not External
**API not working?** → Check VITE_API_URL includes `/api`

## 📚 Detailed Guides

- **GitHub**: See `GITHUB_SETUP.md`
- **Render**: See `RENDER_SETUP.md`
- **Vercel**: See `VERCEL_SETUP.md`

