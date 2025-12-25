# Guest Authentication Setup Guide

## How Guest Authentication Works

There are **two ways** guests can get a username and password:

### Option 1: Self-Registration (Recommended)
Guests create their own account when they RSVP:
1. Guest visits your wedding site (`/`)
2. They see the RSVP form
3. They fill in:
   - Username (they choose)
   - Password (they choose)
   - Personal information
   - RSVP details
4. Account is created automatically
5. They can login later at `/login` to update their RSVP

### Option 2: Manual Creation (For Pre-invited Guests)
You can create guest accounts manually using Render Shell.

## Creating Guest Accounts in Render

### Step 1: Access Render Shell

1. Go to **Render Dashboard** → Your Backend Service
2. Click on the **"Shell"** tab (or "Logs" tab, then look for Shell option)
3. This opens a terminal/command line interface

### Step 2: Run the Guest Creation Script

```bash
cd wedding-planner-backend
python create_guest.py
```

### Step 3: Follow the Prompts

The script will ask you for:
- **Username**: Choose a unique username for the guest
- **Password**: Set a secure password
- **First Name**: Guest's first name
- **Last Name**: Guest's last name
- **Email**: Guest's email address
- **Phone**: (Optional) Guest's phone number

Example:
```
Enter username: johnsmith
Enter password: SecurePass123!
Enter first name: John
Enter last name: Smith
Enter email: john.smith@example.com
Enter phone (optional): +1234567890
```

### Step 4: Share Credentials

After creating the account, share the username and password with the guest so they can:
- Login at `/login` to access their RSVP
- Update their information
- View wedding details

## Alternative: Create Multiple Guests via Script

If you need to create many guest accounts, you can modify the script or create a bulk import script.

## Guest Login Flow

1. Guest visits: `https://your-vercel-url.vercel.app/login`
2. Enters username and password
3. Gets access to:
   - RSVP form (to update their information)
   - Wedding information page
   - Their personal dashboard

## Security Notes

- Each guest has their own username/password
- Passwords are hashed and stored securely
- Guests can only see/update their own information
- Admin can see all guests in the admin dashboard

## Troubleshooting

### "Username already exists"
- Choose a different username
- Or update the existing guest account instead

### "Email already exists"
- The email is already registered
- Guest should use the existing account or reset password

### Can't access Render Shell
- Make sure you're in the correct service
- Try refreshing the page
- Check Render documentation for shell access

## Quick Reference

**Create Guest Account:**
```bash
cd wedding-planner-backend
python create_guest.py
```

**Guest Login URL:**
```
https://your-vercel-url.vercel.app/login
```

**Admin Dashboard:**
```
https://your-vercel-url.vercel.app/admin/dashboard
```

