import cv2
import numpy as np
import time
import math
from HandTracking import HandTrackingModule as htm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# initialize pycaw to control the volume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()

# using hand detector
detector = htm.handDetector(detectionCon=0.7)

# params
widthCam, heightCam = 640, 480
preTime = 0
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
barY1, barY2 = 400, 150
volBar = barY1
volPer = 0

cap = cv2.VideoCapture(0)
cap.set(3, widthCam)
cap.set(4, heightCam)

print("press 'q' to quit")

while True:
    success, img = cap.read()
    img = detector.findHands(img) # detect 21 key point of each hand
    landMarkList = detector.findPosition(img, draw = False)
    
    # we only need landmark of number 4 and 8(4 for thumb, 8 for index_finger_tip)
    if len(landMarkList) != 0:
        # print(landMarkList[4], landMarkList[8])
        x1, y1 = landMarkList[4][1], landMarkList[4][2] # for thumb's coordinates
        x2, y2 = landMarkList[8][1], landMarkList[8][2] # for index's coordinates
        centX, centY = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
        cv2.circle(img,(x2,y2),15,(255,0,255),cv2.FILLED)
        cv2.line(img,(x1, y1),(x2,y2),(255,0,255),3)
        cv2.circle(img,(centX,centY),15,(255,0,255),cv2.FILLED)

        # length from index to thumb
        length = math.hypot(x2 - x1, y2 - y1)

        # hand range 50 - 280
        # volume range -65 - 0,
        # we can use numpy to convert hand range to volume range
        vol = np.interp(length,[50,280],[minVol,maxVol])
        volBar = np.interp(vol,[minVol,maxVol],[barY1, barY2])
        volPer = np.interp(length,[50,280],[0,100])
        print(vol)
        volume.SetMasterVolumeLevel(vol, None)

        if length < 50:
            cv2.circle(img,(centX,centY),15,(0,255,0),cv2.FILLED)

    # plot the volume bar
    cv2.rectangle(img, (50,barY2), (85,barY1), (0,0,255), 4) 
    cv2.rectangle(img, (50,int(volBar)), (85,barY1), (0,0,255), cv2.FILLED)
    cv2.putText(img, f'{int(volPer)} %',(40,450),cv2.FONT_HERSHEY_COMPLEX,
        1 , (0,0,255), 3)
    # show the text on the img
    currTime = time.time()
    fps = 1 / (currTime - preTime)
    preTime = currTime
    cv2.putText(img, f'FPS:{int(fps)}',(40,50),cv2.FONT_HERSHEY_COMPLEX,
        1 , (0,0,255), 3)

    cv2.imshow("Img", img)
    key = cv2.waitKey(1) # set 1ms delay
    if key == ord('q'): 
        print("press 'q' to quit")
        quit()
