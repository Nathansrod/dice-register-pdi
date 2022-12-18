#Autor: Nathan Silva Rodrigues
#Disciplina: PDI - EngComp 2022/02
#Data: Dezembro 2022

import cv2
import numpy as np
import blob_detector

detector = blob_detector.create_detector()

def frameToGrey(frame):
    greyFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return greyFrame

def binarizeFrame(frame):
    frame = frameToGrey(frame)
    ret, binFrame = cv2.threshold(frame,48,255,cv2.THRESH_BINARY)
    return binFrame

def detectBlobs(frame):
    keypoints = detector.detect(frame)
    frame_keypoints = cv2.drawKeypoints(frame, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    return len(keypoints), frame_keypoints

def filterRedDice(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0,60,90]) #0 100 90
    upper_red = np.array([179,255,255]) #179 255 255 w/ yellow sub
    mask = cv2.inRange(hsv, lower_red, upper_red)

    mask_ylw = filterYellowDice(frame)
    mask = mask - mask_ylw
    return mask

def filterWhiteDice(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_white = np.array([0,0,150]) #90 20 150
    upper_white = np.array([179,45,255]) #155 255 255
    mask = cv2.inRange(hsv, lower_white, upper_white)
    return mask

def filterYellowDice(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_yellow = np.array([20,120,90]) #20
    upper_yellow = np.array([40,255,255]) #40
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    return mask

def improveImgYlwRed(frame):
    #Improve image quality
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2,2))
    sharpen_kernel = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])
    frame = cv2.GaussianBlur(frame,(3,3),0)
    frame = cv2.morphologyEx(frame, cv2.MORPH_CLOSE, kernel)
    frame = cv2.filter2D(frame, -1, sharpen_kernel)
    return frame

def improveImgWht(frame):
    #Improve image quality
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2,2))
    sharpen_kernel = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])
    frame = cv2.GaussianBlur(frame,(3,3),0)
    frame = cv2.morphologyEx(frame, cv2.MORPH_CLOSE, kernel)
    frame = cv2.filter2D(frame, -1, sharpen_kernel)
    return frame


#Autor: Nathan Silva Rodrigues
#Disciplina: PDI - EngComp 2022/02
#Data: Dezembro 2022