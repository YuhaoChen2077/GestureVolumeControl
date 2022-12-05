import cv2
import mediapipe as mp
import time
import HandTracking.HandTrackingModule as htm

pTime = 0
cTime = 0
cap = cv2.VideoCapture(0)
detector = htm.handDetector()
while True:
    success, img = cap.read()
    img  = detector.findHands(img/scratch/lh3317/data/eye/raw
    )
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        print(lmList[4])
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    text = "FPS:" + str(int(fps))
    cv2.putText(img, text, (10, 70), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,255), 2)
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord('q'):
        quit()