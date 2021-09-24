import cv2
import mediapipe as mp
import time
import numpy as np
import pyautogui
import os

from datetime import date




myPoints = []

brushThickness = 15
eraserThickness = 50

class handDetector():
#This class has methods: findHands,findPosition
    def __init__ (self, mode=False,MaxNumOfHands=2,DetectionConfidnc=0.5,TrackConfidnc=0.6):
        self.mode = mode
        self.MaxNumOfHands = MaxNumOfHands
        self.DetectionConfidnc = DetectionConfidnc
        self.TrackConfidnc=TrackConfidnc

        self.mpHands=mp.solutions.hands
        self.hands=self.mpHands.Hands( self.mode, self.MaxNumOfHands, self.DetectionConfidnc, self.TrackConfidnc)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]
        
    def findHands(self,img,draw=True):    
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        #print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks: #gives result for all(2) hands
            #handLMs are 21 points. so we need conection too-->mpHands.HAND_CONNECTIONS
                if draw: # if draw=True
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS) #drawing points and lines(=handconections)
        return img 
    
    def findPosition(self, img, handNo=0, draw=True):
        self.lmlist=[] #landmark list
        if self.results.multi_hand_landmarks:
            myHand= self.results.multi_hand_landmarks[handNo] #selecting specific hand, != all hand
            for id, lm in enumerate(myHand.landmark):#landamarks for selected hand
                #print(id, lm)
                #lm = x,y cordinate of each landmark in float numbers. lm.x, lm.y methods
                #So, need to covert in integer
                h, w, c =img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                #print(id, cx, cy)
                self.lmlist.append([id,cx,cy])
                if draw:
                    if(id == 8):
                        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        return self.lmlist

    def fingersUp(self):
        fingers = []

        # print(self.lmlist)
        # Thumb
        if(len(self.lmlist) >0 ):
            if self.lmlist[self.tipIds[0]][1] > self.lmlist[self.tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            # Fingers
            for id in range(1, 5):
                if self.lmlist[self.tipIds[id]][2] < self.lmlist[self.tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

                # totalFingers = fingers.count(1)

        return fingers

def drawOnCanvas(img,myPoints):
    # for point in myPoints:
    #     # cv2.line(img, (point[1], point[2]), (prpoint[1], prpoint[2]), (255, 0, 255), cv2.FILLED)
    #     cv2.circle(img, (point[1], point[2]), 15,(255, 0, 255), cv2.FILLED) 

    for i in range(1, len(myPoints)):
        cv2.line(img, (myPoints[i][1], myPoints[i][2]), (myPoints[i-1][1], myPoints[i-1][2]), (255, 0, 255), 9)

def sceenshotsaving ():
    today = date.today()
    print( today)
    date_time = today.strftime("%m/%d/%Y,%H:%M:%S") + ".PNG"
    print( date_time)

    image = pyautogui.screenshot()
    image.save("screenshot.PNG")



def main():

    folderPath = "Header" 

    myList = os.listdir(folderPath)
    # print(myList)
    overlayList = []
    for imPath in myList:
        image = cv2.imread(f'{folderPath}/{imPath}')
        overlayList.append(image)
    # print(len(overlayList))
    header = overlayList[0]
    
    colorpath = "colors"
    colorlist = os.listdir(colorpath)
    print(colorlist)
    colorimages = []
    for imPath in colorlist:
        image = cv2.imread(f'{colorpath}/{imPath}')
        colorimages.append(image)
    print(len(colorimages))
    blueimage = colorimages[0]
    blueselect = colorimages[1]


    frameWidth = 1280
    frameHeight = 720
    cap = cv2.VideoCapture(0)
    cap.set(3, frameWidth)
    cap.set(4, frameHeight)
    pTime = 0
    cTime = 0
    xp, yp= 0,0
    xforline ,yforline = 0,0  
    drawline = False
    imgCanvas = np.zeros((720, 1280, 3), np.uint8)
    i = 0
    drawColor = (255, 0, 255)
    isblue = False 


    detector=handDetector(DetectionConfidnc=0.85)

    while True:
        success, img = cap.read()
        img= cv2.flip(img,1)
        img=detector.findHands(img)
        lmlist= detector.findPosition(img)
        # OLD CODE 
        # if len(lmlist)!=0:
        #     for newp in lmlist:
        #         myPoints.append(newp)


        fingers = detector.fingersUp()
        if(len(fingers) > 0):
            x1, y1 = lmlist[8][1:]
            x2, y2 = lmlist[12][1:]
            
            # #TO see if thumb and first finger is touched or not 
            
            # #for diffrence 
            # xthumb,ythumb = lmlist[4][1:]
            # xdif =xthumb - x1
            # ydif =ythumb - y1
            # if(xdif<40 and xdif > -40):
            #     # print("x - ayya ")
            #     if(ydif<40 and ydif > -40):
            #         print("touched" + str(i))
            #         i+=1
            # # print(xthumb - x1 )
            # # print(ythumb - y1 )


            # #clicked on the SS image 
            # if x1<216 and y1< 233 :
            #     # sceenshotsaving()
            #     drawline = True
            #     print("made true ")

            #clicked on the blue image 
            if x1<216 and y1> 233 and y1<233+125:
                print("clicked on blue")
                # if isblue :
                #     print(" making blue false ")
                #     isblue = False
                #     drawColor = (255, 0, 255)    
                # else: 
                drawColor = (0,0,255)
                isblue = True
                print(" making blue true ")
                

            if xp == 0 and yp == 0:
                xp = x1
                yp = y1
           
            # # middle finger case 
            # if fingers[1] == False and fingers[2] and fingers[3] == False and fingers[4] == False and drawline :
            #     if xforline == 0 and yforline == 0:
            #         print("got one x ")
            #         xforline , yforline = lmlist[12][1:] 
            #         cv2.circle(img, (xforline , yforline), 15, drawColor, cv2.FILLED)
            #     # else :
            #     #     print("fucked ")
            #     #     xnow,ynow = lmlist[12][1:]                  
            #     #     cv2.line(img, (xforline , yforline), (xnow,ynow), drawColor, brushThickness)
            #     #     cv2.line(imgCanvas, (xforline , yforline), (xnow,ynow), drawColor, brushThickness)
            #     #     drawline = False 
            
            
            # #thumb and first finger touch case
            # if drawline and xforline != 0 and yforline != 0:
            #     xthumb,ythumb = lmlist[4][1:]
            #     xdif =xthumb - x1
            #     ydif =ythumb - y1

            #     if(xdif<40 and xdif > -40):
            #         # print("x - ayya ")
            #         if(ydif<40 and ydif > -40):
            #             print("well done bhai ")
            #             xnow,ynow = lmlist[12][1:]                  
            #             cv2.line(img, (xforline , yforline), (xnow,ynow), drawColor, brushThickness)
            #             cv2.line(imgCanvas, (xforline , yforline), (xnow,ynow), drawColor, brushThickness)
            #             drawline = False 

            
            
            if fingers[1] and fingers[2] and fingers[3] == False and fingers[4] == False :
                # print("erasing this ")
                cv2.line(img, (xp, yp), (x1, y1), (0, 0, 0), eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), (0, 0, 0), eraserThickness)
                cv2.line(img, (xp, yp), (x2, y2), (0, 0, 0), eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x2, y2), (0, 0, 0), eraserThickness)

            if fingers[1] and fingers[2] == False and fingers[3] == False and fingers[4] == False :
                cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
                # print("Drawing Mode")
                if xp == 0 and yp == 0:
                    xp = x1
                    yp = y1

                # cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)

                # if drawColor == (0, 0, 0):
                #     cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                #     cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
                
            
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
            # if fingers[1] and fingers[2] and fingers[3] and fingers[4]:
                # sceenshotsaving()
                # image = pyautogui.screenshot()
                # image.save("screenshot.PNG")
 
            xp, yp = x1, y1


        imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
        _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
        imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
        img = cv2.bitwise_and(img,imgInv)
        img = cv2.bitwise_or(img,imgCanvas)

    



        #Write frame rate
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, "FPS= " + str(int(fps)), (10, 20), cv2.FONT_HERSHEY_PLAIN, 1,(0, 0, 0), 1)

        #put header 
        img[0:233, 0:216] = header
        #put colors for drawing 
        if isblue:
            img[233:233+125,0:125] = blueselect
        else :
            img[233:233+125,0:125] = blueimage

        cv2.imshow('image', img)
        if cv2.waitKey(1) == 27:
            break

if __name__ == "__main__":
    main()



##########################################################################################################

