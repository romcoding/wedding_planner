# GitHub Setup Guide

## Step 1: Create GitHub Repository

1. Go to [GitHub](https://github.com) and sign in
2. Click the **"+"** icon in the top right → **"New repository"**
3. Fill in the details:
   - **Repository name**: `wedding-planner` (or your preferred name)
   - **Description**: "Full-stack wedding planning application"
   - **Visibility**: Choose Public or Private
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
4. Click **"Create repository"**

## Step 2: Connect Local Repository to GitHub

After creating the repository, GitHub will show you commands. Use these:

```bash
cd /Users/romanhess/Coding/wedding_planner

# Add the remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/wedding-planner.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

**Alternative (if you prefer SSH):**
```bash
git remote add origin git@github.com:YOUR_USERNAME/wedding-planner.git
git branch -M main
git push -u origin main
```

## Step 3: Verify

1. Go to your GitHub repository page
2. You should see all your files
3. The repository is now ready for deployment!

## Next Steps

After pushing to GitHub:
1. Follow the **Render Setup Guide** below
2. Then follow the **Vercel Setup Guide**

