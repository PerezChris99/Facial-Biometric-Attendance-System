import cv2
import numpy as np
import face_recognition

imgElon = face_recognition.load_image_file('ImageBasics/')
imgElon = cv2.cvtColor(imgElon, cv2.COLOR_BGR2RGB)
imgTest = face_recognition.load_image_file('ImagesBasic/')
imgTest = cv2.cvtColor(imgTest, cv2.COLOR_BGR2RGB)

cv2.imshow('Elon Musk', imgElon)
cv2.waitKey(0)