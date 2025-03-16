import os
import sys
import subprocess

def check_requirements():
    """Check if all required packages are installed."""
    print("Checking requirements...")
    
    try:
        # Try to install requirements
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("All requirements installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("Error installing requirements. Please install them manually.")
        return False

def check_directories():
    """Check if all required directories exist."""
    print("Checking directories...")
    
    required_dirs = [
        "Images",
        "Resources",
        "Resources/Modes",
        "ImagesBasic"
    ]
    
    for directory in required_dirs:
        if not os.path.exists(directory):
            print(f"Creating directory: {directory}")
            os.makedirs(directory, exist_ok=True)
    
    print("All directories created!")
    return True

def check_firebase_config():
    """Check if Firebase config exists."""
    print("Checking Firebase configuration...")
    
    if not os.path.exists("serviceAccountKey.json"):
        print("WARNING: serviceAccountKey.json not found!")
        print("Please download your Firebase service account key and save it as serviceAccountKey.json")
        return False
    
    print("Firebase configuration found!")
    return True

def setup():
    """Run the setup process."""
    print("Starting setup for Facial Biometric Attendance System...")
    
    requirements_ok = check_requirements()
    directories_ok = check_directories()
    firebase_ok = check_firebase_config()
    
    if requirements_ok and directories_ok and firebase_ok:
        print("\nSetup completed successfully!")
        print("\nNext steps:")
        print("1. Add student images to the 'Images' folder (filename should be student ID, e.g., 123456.png)")
        print("2. Run AddDatatoDatabase.py to populate the database with student data")
        print("3. Run EncodeGenerator.py to generate face encodings")
        print("4. Run main.py to start the attendance system")
    else:
        print("\nSetup completed with warnings. Please address the issues above before running the system.")

if __name__ == "__main__":
    setup()
