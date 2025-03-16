# Facial Biometric Attendance System

A modern attendance system using facial recognition technology that automatically records student attendance and updates a Firebase database in real-time.

## Features

- Real-time face detection and recognition
- Firebase database integration for storing student information
- Firebase storage integration for storing student images
- Automatic attendance tracking
- User-friendly interface

## System Requirements

- Python 3.8 or higher
- Webcam
- Internet connection for Firebase integration

## Setup Instructions

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a Firebase project and download the service account key:
   - Go to the Firebase console (https://console.firebase.google.com/)
   - Create a new project
   - Go to Project Settings > Service Accounts
   - Generate a new private key and save it as `serviceAccountKey.json` in the project root

4. Set up the Firebase Realtime Database:
   - Create a Realtime Database in your Firebase project
   - Set up the database rules to allow read/write access
   - Run `AddDatatoDatabase.py` to populate the database with sample data

5. Set up Firebase Storage:
   - Enable Firebase Storage in your Firebase project
   - Create a folder named `Images` in your project
   - Add student images to the `Images` folder (filename should be the student ID, e.g., `123456.png`)

6. Generate encodings:
   - Run `EncodeGenerator.py` to encode all student faces and upload them to Firebase

7. Run the main application:
   - Run `main.py` to start the attendance system

## Directory Structure

- `main.py`: Main application file
- `EncodeGenerator.py`: Generates encodings for student faces
- `AddDatatoDatabase.py`: Adds student data to Firebase database
- `Basics.py`: Basic face recognition test script
- `Images/`: Folder for student images
- `Resources/`: Contains background images and UI elements
- `Resources/Modes/`: Contains UI mode images

## Usage

1. Run the main application:
   ```
   python main.py
   ```
2. The system will automatically detect faces and mark attendance
3. Student information and attendance records will be updated in real-time in the Firebase database

## Troubleshooting

- Make sure you have a working webcam
- Ensure your `serviceAccountKey.json` is correctly configured
- Check your Firebase database and storage permissions
- If face recognition is not working, try adjusting lighting conditions
