"""
Setup script for Customer Feedback Intelligence System
This script will create a virtual environment and install dependencies
"""

import subprocess
import sys
import os

def run_command(command):
    """Run a command and return the result"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def setup_environment():
    """Setup the development environment"""
    print("Setting up Customer Feedback Intelligence System...")
    
    # Check if venv already exists
    if not os.path.exists('venv'):
        print("Creating virtual environment...")
        success, stdout, stderr = run_command(f'{sys.executable} -m venv venv')
        if not success:
            print(f"Failed to create virtual environment: {stderr}")
            print("Please ensure Python is properly installed and accessible")
            return False
        print("Virtual environment created successfully!")
    else:
        print("Virtual environment already exists!")
    
    # Determine the pip path based on OS
    if os.name == 'nt':  # Windows
        pip_path = os.path.join('venv', 'Scripts', 'pip')
        python_path = os.path.join('venv', 'Scripts', 'python')
    else:  # Unix/Linux/MacOS
        pip_path = os.path.join('venv', 'bin', 'pip')
        python_path = os.path.join('venv', 'bin', 'python')
    
    # Install requirements
    print("Installing dependencies...")
    success, stdout, stderr = run_command(f'{pip_path} install -r requirements.txt')
    if not success:
        print(f"Failed to install dependencies: {stderr}")
        return False
    print("Dependencies installed successfully!")
    
    # Generate data
    print("Generating sample data...")
    success, stdout, stderr = run_command(f'{python_path} generate_feedback_data.py')
    if not success:
        print(f"Failed to generate data: {stderr}")
        return False
    print("Sample data generated successfully!")
    
    print("\nSetup completed successfully!")
    print("\nTo run the application:")
    print(f"1. Activate virtual environment: {python_path}")
    print("2. Run the dashboard: python app.py")
    
    return True

if __name__ == "__main__":
    setup_environment()
