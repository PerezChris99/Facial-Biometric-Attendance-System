import cv2
import numpy as np
import face_recognition

imgElon = face_recognition.load_image_file('ImagesBasic/Elon.jpg')
imgElon = cv2.cvtColor(imgElon, cv2.COLOR_BGR2RGB)
imgTest = face_recognition.load_image_file('ImagesBasic/ElonTest.jpg')
imgTest = cv2.cvtColor(imgTest, cv2.COLOR_BGR2RGB)

# Find faces in images
faceLocElon = face_recognition.face_locations(imgElon)[0]
encodeElon = face_recognition.face_encodings(imgElon)[0]
cv2.rectangle(imgElon, (faceLocElon[3], faceLocElon[0]), (faceLocElon[1], faceLocElon[2]), (255, 0, 255), 2)

faceLocTest = face_recognition.face_locations(imgTest)[0]
encodeTest = face_recognition.face_encodings(imgTest)[0]
cv2.rectangle(imgTest, (faceLocTest[3], faceLocTest[0]), (faceLocTest[1], faceLocTest[2]), (255, 0, 255), 2)

# Compare faces
results = face_recognition.compare_faces([encodeElon], encodeTest)
faceDis = face_recognition.face_distance([encodeElon], encodeTest)
print(results, faceDis)
cv2.putText(imgTest, f'{results[0]} {round(faceDis[0], 2)}', (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)

cv2.imshow('Elon', imgElon)
cv2.imshow('Elon Test', imgTest)
cv2.waitKey(0)