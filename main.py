import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy

wcam, hcam = 720,640
frameR = 100 # frame reduction
cap = cv2.VideoCapture(0)
cap.set(3,wcam)
cap.set(4,hcam)
ptime = 0
detector= htm.handDetector(maxHands=1)

wScr, hScr = autopy.screen.size()

# print(wScr,hScr)
while True:
    #s1) find hand landmarks
    success, img =cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)
    # s2)get tip of index and middle finger i.e. point no. 8 and 12
    if len(lmList)!=0:

        x1, y1 = lmList[8][1:]
    #     this means that we want tip no. 8 and element no. 0 to 1 i.e 1:
        x2,y2 = lmList[12][1:]

        # print(x1,y1,x2,y2)


    # s3)check which fingers are up
        fingers = detector.fingersUp()
        # print(fingers)
        cv2.rectangle(img, (frameR, frameR), (wcam - frameR, hcam - frameR),(255,0,255),2)
        # s4) only index finger:moving mode
        if fingers[1] ==1 and fingers[2]==0:



            # s5) convert coordinates

            x3 = np.interp(x1,(frameR,wcam-frameR),(0,hScr))
            y3 = np.interp(y1, (frameR,hcam-frameR),(0,hScr))

    # s6) smoothen values

    # s7) move mouse
            autopy.mouse.move(x3, y3)
            cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
    #  s8) check in clicking mode: 8 and 12 are up or not
        if fingers[1]==1 and fingers[2]==1:
            length, img, _ = detector.findDistance(8,12,img)
            print(length)
    #  s9) find distance

    #  s10) click mouse if distance short

    #  s11) frame rate
    ctime= time.time()
    fps = 1/(ctime - ptime)
    ptime = ctime
    cv2.putText(img,str(int(fps)),(20,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)

    #  s12) display control
    cv2.imshow("Image",img)
    cv2.waitKey(1)