import argparse
import getpass
import sys
from app import create_app
from app.extensions import db
from app.models import User

def create_admin():
    parser = argparse.ArgumentParser(description="Create Platform Admin")
    parser.add_argument("--name", help="Full Name of the admin")
    parser.add_argument("--email", help="Email address")
    parser.add_argument("--password", help="Password")
    args = parser.parse_args()

    app = create_app()
    with app.app_context():
        print("--- Create Platform Admin ---")
        
        full_name = args.name or input("Enter Full Name: ").strip()
        if not full_name:
            print("Full name is required.")
            sys.exit(1)
            
        email = args.email or input("Enter Email Address: ").strip()
        if not email:
            print("Email is required.")
            sys.exit(1)
            
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            print("Error: Email already exists.")
            sys.exit(1)
            
        password = args.password or getpass.getpass("Enter Password (min 6 chars): ")
        if len(password) < 6:
            print("Error: Password must be at least 6 characters.")
            sys.exit(1)
            
        if not args.password:
            confirm_password = getpass.getpass("Confirm Password: ")
            if password != confirm_password:
                print("Error: Passwords do not match.")
                sys.exit(1)
            
        # Create user
        admin_user = User(
            full_name=full_name,
            email=email,
            role='platform_admin',
            is_active=True
        )
        admin_user.set_password(password)
        
        db.session.add(admin_user)
        db.session.commit()
        
        print(f"\nSuccess! Platform Admin '{full_name}' ({email}) created successfully.")

if __name__ == '__main__':
    create_admin()
