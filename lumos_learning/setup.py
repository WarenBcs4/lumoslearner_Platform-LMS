#!/usr/bin/env python3
"""
Lumos Learning Setup Script
This script helps set up the development environment for Lumos Learning LMS.
"""

import os
import sys
import subprocess
import secrets
import string

def generate_secret_key():
    """Generate a random secret key for Django"""
    alphabet = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
    return ''.join(secrets.choice(alphabet) for i in range(50))

def create_env_file():
    """Create .env file from .env.example with generated secret key"""
    if os.path.exists('.env'):
        print("✓ .env file already exists")
        return
    
    if not os.path.exists('.env.example'):
        print("✗ .env.example file not found")
        return
    
    with open('.env.example', 'r') as f:
        content = f.read()
    
    # Replace placeholder secret key with generated one
    secret_key = generate_secret_key()
    content = content.replace('your-super-secret-key-here', secret_key)
    
    with open('.env', 'w') as f:
        f.write(content)
    
    print("✓ Created .env file with generated secret key")

def install_dependencies():
    """Install Python dependencies"""
    print("Installing Python dependencies...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
        print("✓ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("✗ Failed to install dependencies")
        return False
    return True

def run_migrations():
    """Run Django migrations"""
    print("Running database migrations...")
    try:
        subprocess.run([sys.executable, 'manage.py', 'migrate'], check=True)
        print("✓ Migrations completed successfully")
    except subprocess.CalledProcessError:
        print("✗ Failed to run migrations")
        return False
    return True

def create_superuser():
    """Create Django superuser"""
    print("\nCreating superuser account...")
    print("Please provide the following information:")
    try:
        subprocess.run([sys.executable, 'manage.py', 'createsuperuser'], check=True)
        print("✓ Superuser created successfully")
    except subprocess.CalledProcessError:
        print("✗ Failed to create superuser")
        return False
    except KeyboardInterrupt:
        print("\n✗ Superuser creation cancelled")
        return False
    return True

def collect_static():
    """Collect static files"""
    print("Collecting static files...")
    try:
        subprocess.run([sys.executable, 'manage.py', 'collectstatic', '--noinput'], check=True)
        print("✓ Static files collected successfully")
    except subprocess.CalledProcessError:
        print("✗ Failed to collect static files")
        return False
    return True

def main():
    """Main setup function"""
    print("🚀 Setting up Lumos Learning LMS...")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('manage.py'):
        print("✗ manage.py not found. Please run this script from the project root directory.")
        sys.exit(1)
    
    # Create .env file
    create_env_file()
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Run migrations
    if not run_migrations():
        sys.exit(1)
    
    # Collect static files
    if not collect_static():
        sys.exit(1)
    
    # Create superuser
    create_superuser()
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Start the development server: python manage.py runserver")
    print("2. Visit http://127.0.0.1:8000 to see your application")
    print("3. Visit http://127.0.0.1:8000/admin to access the admin panel")
    print("\nFor production deployment, see the README.md file.")

if __name__ == '__main__':
    main()