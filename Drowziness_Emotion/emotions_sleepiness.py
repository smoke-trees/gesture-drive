# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 15:47:14 2019

@author: Unnikrishnan Menon
"""

import imutils
from keras.models import load_model
import numpy as np
from imutils import face_utils
#import serial
import cv2
import dlib
from scipy.spatial import distance

def aspect_ratio(eye):
	return (distance.euclidean(eye[1],eye[5])+distance.euclidean(eye[2],eye[4]))/(2.0*distance.euclidean(eye[0],eye[3]))

#Arduino_Serial=serial.Serial('COM5',9600)
t=0
model=load_model('my_model.hdf5')
fc=cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')
emotion=['angry','disgust','fear','happy','sad','yawn','neutral']

detect=dlib.get_frontal_face_detector()
predict=dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

(l_0,l_n)=face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(r_0,r_n)=face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
	
cap=cv2.VideoCapture(0)
while(True):
    _,frame=cap.read()
    frame=imutils.resize(frame,width=450)
    frame=cv2.flip(frame,1)
    grey_img=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    face=detect(grey_img,0)
    for i in face:
        mappings=predict(grey_img,i)
        mappings=face_utils.shape_to_np(mappings)
        
        right_eye=mappings[r_0:r_n]
        left_eye=mappings[l_0:l_n]
        
        right_AR=aspect_ratio(right_eye)
        left_AR=aspect_ratio(left_eye)
        
        right_hull=cv2.convexHull(right_eye)
        left_hull=cv2.convexHull(left_eye)
    
        cv2.drawContours(frame,[right_hull],-1,(0,0,255),1)
        cv2.drawContours(frame,[left_hull],-1,(0,0,255),1)
        AR=(left_AR+right_AR)/(2.0)
        if AR<0.25:
            if t>=15:
                cv2.putText(frame,"WAKE UP!",(10,30),cv2.FONT_HERSHEY_COMPLEX,0.7,(255,0,0),2)
                #print('LED: ON')                
                #Arduino_Serial.write(1)    
            t+=1
        else:
            #Arduino_Serial.write(0)
            t=0
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    det_face=fc.detectMultiScale(gray,scaleFactor=1.1)
    for (x, y, w, h) in det_face:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        box=frame[y:y+h,x:x+w]
        box=cv2.resize(box,(48,48))
        box=cv2.cvtColor(box,cv2.COLOR_BGR2GRAY)
        box=box.astype('float32')/255
        box=np.asarray(box)
        box=box.reshape(1, 1,box.shape[0],box.shape[1])
        emo=emotion[np.argmax(model.predict(box))]
        cv2.putText(frame,emo,(300,30),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,255,0),2,cv2.LINE_AA)
        if emo=='yawn':
            cv2.putText(frame,"WAKE UP!",(10,30),cv2.FONT_HERSHEY_COMPLEX,0.7,(255,0,0),2)
    cv2.imshow("Frame",frame)
    key_pressed=cv2.waitKey(1) & 0xFF
    if key_pressed==ord("q"):
        cv2.destroyAllWindows()
        cap.release()
        break

    