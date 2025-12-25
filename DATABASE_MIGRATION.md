# Database Migration Guide

## Problem

The database is missing the `username` and `password_hash` columns that were added to the Guest model. This happens when the database was created before we added guest authentication.

## Solution: Run Migration Script

### Step 1: Access Render Shell

1. Go to **Render Dashboard** → Your Backend Service
2. Click on the **"Shell"** tab
3. This opens a terminal

### Step 2: Run the Migration

```bash
cd wedding-planner-backend
python migrate_add_guest_auth.py
```

### Step 3: Verify

The script will:
- ✅ Add `username` column to guests table
- ✅ Add `password_hash` column to guests table  
- ✅ Create an index on username for faster lookups
- ✅ Show success message

### Step 4: Create Guest Accounts

After migration, you can create guest accounts:

```bash
python create_guest.py
```

## What the Migration Does

The migration script:
1. Checks if columns already exist (safe to run multiple times)
2. Adds `username VARCHAR(80) UNIQUE` column
3. Adds `password_hash VARCHAR(255)` column
4. Creates an index on username for performance

## Troubleshooting

### "Columns already exist"
- This means the migration already ran
- You can proceed to create guest accounts
- Safe to ignore

### "Permission denied"
- Make sure you're running in Render Shell
- Check that you're in the correct directory
- Verify database connection

### Other Errors
- Check Render logs for more details
- Ensure database is accessible
- Verify you're using the correct database

## Alternative: Manual SQL (Advanced)

If the script doesn't work, you can run SQL directly:

```sql
ALTER TABLE guests ADD COLUMN IF NOT EXISTS username VARCHAR(80) UNIQUE;
ALTER TABLE guests ADD COLUMN IF NOT EXISTS password_hash VARCHAR(255);
CREATE INDEX IF NOT EXISTS ix_guests_username ON guests(username);
```

## After Migration

Once migration is complete:
1. ✅ Guest authentication will work
2. ✅ You can create guest accounts
3. ✅ Guests can register with username/password
4. ✅ Guests can login at `/login`

