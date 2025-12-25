#!/usr/bin/env python3
"""
Migration script to add username and password_hash columns to guests table.
Run this once to update your existing database schema.
"""

from src.main import create_app
from src.models import db
from sqlalchemy import text

def migrate():
    app = create_app()
    
    with app.app_context():
        print("=" * 50)
        print("Database Migration: Adding Guest Authentication Columns")
        print("=" * 50)
        print()
        
        try:
            # Check if columns already exist
            result = db.session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='guests' AND column_name='username'
            """))
            
            if result.fetchone():
                print("⚠️  Columns already exist. Migration not needed.")
                return
            
            print("Adding username and password_hash columns to guests table...")
            
            # Add username column
            db.session.execute(text("""
                ALTER TABLE guests 
                ADD COLUMN username VARCHAR(80) UNIQUE
            """))
            print("✅ Added 'username' column")
            
            # Add password_hash column
            db.session.execute(text("""
                ALTER TABLE guests 
                ADD COLUMN password_hash VARCHAR(255)
            """))
            print("✅ Added 'password_hash' column")
            
            # Create index on username for faster lookups
            db.session.execute(text("""
                CREATE INDEX IF NOT EXISTS ix_guests_username ON guests(username)
            """))
            print("✅ Created index on 'username' column")
            
            db.session.commit()
            
            print()
            print("=" * 50)
            print("✅ Migration completed successfully!")
            print("=" * 50)
            print()
            print("You can now create guest accounts with usernames and passwords.")
            
        except Exception as e:
            db.session.rollback()
            print()
            print("=" * 50)
            print("❌ Migration failed!")
            print("=" * 50)
            print(f"Error: {str(e)}")
            print()
            print("If columns already exist, this is normal. The migration is safe to run multiple times.")
            raise

if __name__ == '__main__':
    migrate()

