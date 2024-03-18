from threading import Thread
import time
from datetime import datetime
import pyautogui
import cv2
import numpy as np
import os
from utils.Constants import BASE_IMAGE_DIR

class SessionThread(Thread):
    def __init__(self,newSessionWidget,session_uuid):
        super().__init__()
        self.session_uuid = session_uuid
        self.newSessionWidget = newSessionWidget
        self.isRunning = True
        self.isPause = False

    def setTimer(self):
        current = datetime.now()
        FMT = '%H:%M:%S'
        difference = current - self.startTime            
        hours = int(difference.total_seconds()//3600)
        minutes = int(difference.total_seconds()//60)
        seconds = int(difference.total_seconds()%60)
        self.newSessionWidget.durationLBL.setText(" {} : {} : {}".format(hours,minutes,seconds))


    def run(self):
        folder = BASE_IMAGE_DIR + str(self.session_uuid)
        os.makedirs(folder)
        self.startTime = datetime.now()
        current_time = self.startTime.strftime("%H:%M:%S")
        self.newSessionWidget.startTimeLBL.setText(current_time)
        index = 1
        while self.isRunning:
            time.sleep(1)

            screen = pyautogui.screenshot()
            #print(type(screen))
            screen_grey = cv2.cvtColor(np.array(screen), cv2.COLOR_BGR2GRAY)
           
            faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
            faces = faceCascade.detectMultiScale(
                        screen_grey,
                        scaleFactor=1.3,
                        minNeighbors=3,
                        minSize=(48,48))

            print("Found {0} Faces!".format(len(faces)))
            for (x, y, w, h) in faces:                
                roi_color = screen_grey[y:y + h, x:x + w]  
                roi_color = cv2.resize(roi_color, (48,48))  
                cv2.imwrite(folder+'/file'+ str(index) +'.png', roi_color)           
                index+=1

            self.setTimer()