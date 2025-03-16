import os
import pickle
import numpy as np
import cv2
import face_recognition
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import numpy as np
from datetime import datetime

# Import error handling
try:
    from error_handler import log_error, log_info, FaceRecognitionError, DatabaseError
except ImportError:
    # Simple fallback if error_handler.py is not available
    def log_error(msg, exc=None): print(f"ERROR: {msg}") 
    def log_info(msg): print(f"INFO: {msg}")
    class FaceRecognitionError(Exception): pass
    class DatabaseError(Exception): pass

# Initialize Firebase
try:
    if not firebase_admin._apps:
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred, {
            'databaseURL': "https://faceattendancerealtime-default-rtdb.firebaseio.com/",
            'storageBucket': "faceattendancerealtime.appspot.com"
        })
    bucket = storage.bucket()
except Exception as e:
    log_error("Failed to initialize Firebase", e)
    exit(1)

# Initialize webcam
try:
    cap = cv2.VideoCapture(0)  # Try default camera first
    if not cap.isOpened():
        cap = cv2.VideoCapture(1)  # Try secondary camera
    
    if not cap.isOpened():
        raise Exception("No camera available")
        
    cap.set(3, 640)
    cap.set(4, 480)
except Exception as e:
    log_error("Failed to initialize camera", e)
    exit(1)

# Load background image
try:
    imgBackground = cv2.imread('Resources/background.png')
    if imgBackground is None:
        raise Exception("Could not load background image")
except Exception as e:
    log_error("Failed to load background image", e)
    exit(1)

# Load mode images
try:
    folderModePath = 'Resources/Modes'
    modePathList = os.listdir(folderModePath)
    imgModeList = []
    for path in modePathList:
        img = cv2.imread(os.path.join(folderModePath, path))
        if img is not None:
            imgModeList.append(img)
        else:
            log_error(f"Could not load mode image: {path}")
    
    if len(imgModeList) == 0:
        raise Exception("No mode images loaded")
except Exception as e:
    log_error("Failed to load mode images", e)
    exit(1)

# Load encoding file
try:
    log_info("Loading Encode File ...")
    file = open('EncodeFile.p', 'rb')
    encodeListKnownWithIds = pickle.load(file)
    file.close()
    encodeListKnown, studentIds = encodeListKnownWithIds
    log_info("Encode File Loaded")
except Exception as e:
    log_error("Failed to load encoding file", e)
    exit(1)

# Initialize variables
modeType = 0
counter = 0
id = -1
imgStudent = []

log_info("Starting face recognition system...")

while True:
    try:
        success, img = cap.read()
        if not success:
            raise FaceRecognitionError("Failed to read from camera")

        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        faceCurFrame = face_recognition.face_locations(imgS)
        encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

        imgBackground[162:162 + 480, 55:55 + 640] = img
        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

        if faceCurFrame:
            for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

                matchIndex = np.argmin(faceDis)

                if matches[matchIndex]:
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                    imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                    id = studentIds[matchIndex]
                    if counter == 0:
                        cvzone.putTextRect(imgBackground, "Loading", (275, 400))
                        cv2.imshow("Face Attendance", imgBackground)
                        cv2.waitKey(1)
                        counter = 1
                        modeType = 1

            if counter != 0:
                if counter == 1:
                    try:
                        studentInfo = db.reference(f'Students/{id}').get()
                        blob = bucket.get_blob(f'Images/{id}.png')
                        array = np.frombuffer(blob.download_as_string(), np.uint8)
                        imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
                        datetimeObject = datetime.strptime(studentInfo['last_attendance_time'],
                                                           "%Y-%m-%d %H:%M:%S")
                        secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                        if secondsElapsed > 30:
                            ref = db.reference(f'Students/{id}')
                            studentInfo['total_attendance'] += 1
                            ref.child('total_attendance').set(studentInfo['total_attendance'])
                            ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                        else:
                            modeType = 3
                            counter = 0
                            imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
                    except Exception as e:
                        log_error("Failed to update attendance data", e)
                        modeType = 3
                        counter = 0
                        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                if modeType != 3:
                    if 10 < counter < 20:
                        modeType = 2

                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                    if counter <= 10:
                        cv2.putText(imgBackground, str(studentInfo['total_attendance']), (861, 125),
                                    cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                        cv2.putText(imgBackground, str(studentInfo['major']), (1006, 550),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                        cv2.putText(imgBackground, str(id), (1006, 493),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                        cv2.putText(imgBackground, str(studentInfo['standing']), (910, 625),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                        cv2.putText(imgBackground, str(studentInfo['year']), (1025, 625),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                        cv2.putText(imgBackground, str(studentInfo['starting_year']), (1125, 625),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                        (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                        offset = (414 - w) // 2
                        cv2.putText(imgBackground, str(studentInfo['name']), (808 + offset, 445),
                                    cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                        imgBackground[175:175 + 216, 909:909 + 216] = imgStudent

                    counter += 1

                    if counter >= 20:
                        counter = 0
                        modeType = 0
                        studentInfo = []
                        imgStudent = []
                        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
        else:
            modeType = 0
            counter = 0
        cv2.imshow("Face Attendance", imgBackground)
        cv2.waitKey(1)
    except Exception as e:
        log_error("An error occurred during face recognition", e)
        modeType = 0
        counter = 0
        cv2.imshow("Face Attendance", imgBackground)
        cv2.waitKey(1)