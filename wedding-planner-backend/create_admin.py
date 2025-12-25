#!/usr/bin/env python3
"""
Script to create an admin user for the wedding planner application.
Usage: python create_admin.py
"""

from src.main import create_app
from src.models import db, User

def create_admin():
    app = create_app()
    
    with app.app_context():
        print("=" * 50)
        print("Wedding Planner - Admin User Creation")
        print("=" * 50)
        print()
        
        email = input("Enter admin email: ").strip()
        if not email:
            print("Error: Email is required")
            return
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            print(f"Error: User with email '{email}' already exists")
            return
        
        name = input("Enter admin name: ").strip() or email.split('@')[0]
        password = input("Enter password: ").strip()
        
        if not password:
            print("Error: Password is required")
            return
        
        # Create user
        user = User(
            email=email,
            name=name,
            role='admin'
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        print()
        print("=" * 50)
        print("✅ Admin user created successfully!")
        print("=" * 50)
        print(f"Email: {email}")
        print(f"Name: {name}")
        print()
        print("You can now login at /admin/login")

if __name__ == '__main__':
    create_admin()

