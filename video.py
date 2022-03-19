
import cv2
import numpy as np
from pygame import *

mixer.init()

kick = cv2.resize(cv2.imread('kick.jpg', 1), (100,100), interpolation=cv2.INTER_AREA)
snare = cv2.resize(cv2.imread('snare.jpg', 1), (100,100), interpolation=cv2.INTER_AREA)

cap = cv2.VideoCapture(0)
playing2 = False
n = m = 0

while True:
    n = n%10
    m = m%10
    ret, frame = cap.read()
    x11 = 350
    y11 = 50
    x21 = 450
    y21 = 150
    x12,y12,x22,y22 = 350,500,450,600
    box1 = frame[x11:x21, y11:y21]
    box2 = frame[x12:x22,y12:y22]

    hsv1 = cv2.cvtColor(box1, cv2.COLOR_BGR2HSV)
    hsv2 = cv2.cvtColor(box2, cv2.COLOR_BGR2HSV)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # rgb = cv2.cvtColor(box1, cv2.COLOR_BGR2RGB)

    # lower1 = np.array([0])

    lower1 = np.array([0, 100, 20]) 
    upper1 = np.array([10, 255, 255])

    lower2 = np.array([160,100,20])
    upper2 = np.array([179,255,255])

    mask11 = cv2.inRange(hsv1, lower1, upper1)
    mask21 = cv2.inRange(hsv1, lower2, upper2)
    mask1 = mask11+mask21
    mask12 = cv2.inRange(hsv2, lower1, upper1)
    mask22 = cv2.inRange(hsv2, lower2, upper2)
    mask2 = mask12+mask22
    mask = cv2.inRange(hsv, lower1, upper1) + cv2.inRange(hsv, lower2, upper2)
    mask[x11:x21,y11:y21] = mask1
    mask[x12:x22,y12:y22] = mask2

    add_watermark1 = cv2.addWeighted(kick, 0.6, box1, 0.4, 0)
    add_watermark2 = cv2.addWeighted(snare, 0.6, box2, 0.4, 0)
    frame[x11:x21,y11:y21] = add_watermark1
    frame[x12:x22,y12:y22] = add_watermark2

    # cv2.imshow("Mask1", mask1)
    # cv2.imshow("Mask2", mask2)
    cv2.imshow("REDCAM", mask)
    cv2.imshow("WEBCAM", frame)
    
    test1 = np.sum(mask1)/255
    test2 = np.sum(mask2)/255
    if test1>9 and m==0:
        print(test1)
        mixer.music.load('kick.ogg')
        mixer.music.play()
        # while mixer.music.get_busy():
        #     continue
    m=m+1        
        
    if test2>300 and n==0:
        mixer.music.load('snare.ogg')
        mixer.music.play()
    n=n+1
        # if mixer.music.get_busy():
        #     playing2 = True
            
        
    # if np.array_equal(test1, temp, equal_nan = False) or np.array_equal(test2, temp, equal_nan = False) or a==1 or b==1:
    #         break
    # print(np.shape(mask))

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()