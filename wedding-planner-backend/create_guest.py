#!/usr/bin/env python3
"""
Script to create a guest account for the wedding planner application.
Usage: python create_guest.py
"""

from src.main import create_app
from src.models import db, Guest

def create_guest():
    app = create_app()
    
    with app.app_context():
        print("=" * 50)
        print("Wedding Planner - Guest Account Creation")
        print("=" * 50)
        print()
        
        username = input("Enter username: ").strip()
        if not username:
            print("Error: Username is required")
            return
        
        # Check if username already exists
        existing_guest = Guest.query.filter_by(username=username).first()
        if existing_guest:
            print(f"Error: Username '{username}' already exists")
            return
        
        password = input("Enter password: ").strip()
        if not password:
            print("Error: Password is required")
            return
        
        first_name = input("Enter first name: ").strip()
        if not first_name:
            print("Error: First name is required")
            return
        
        last_name = input("Enter last name: ").strip()
        if not last_name:
            print("Error: Last name is required")
            return
        
        email = input("Enter email: ").strip()
        if not email:
            print("Error: Email is required")
            return
        
        # Check if email already exists
        existing_email = Guest.query.filter_by(email=email).first()
        if existing_email:
            print(f"Error: Email '{email}' already exists")
            return
        
        phone = input("Enter phone (optional): ").strip() or None
        
        # Create guest
        guest = Guest(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            rsvp_status='pending'
        )
        guest.set_password(password)
        
        db.session.add(guest)
        db.session.commit()
        
        print()
        print("=" * 50)
        print("✅ Guest account created successfully!")
        print("=" * 50)
        print(f"Username: {username}")
        print(f"Name: {first_name} {last_name}")
        print(f"Email: {email}")
        print()
        print("The guest can now login at /login")

if __name__ == '__main__':
    create_guest()

