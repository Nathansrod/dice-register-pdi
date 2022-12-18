#Autor: Nathan Silva Rodrigues
#Disciplina: PDI - EngComp 2022/02
#Data: Dezembro 2022

import cv2
import image_processing as ip
import numpy as np
import ui
import PySimpleGUI as sg

window = ui.buildUi()

cap = cv2.VideoCapture(1)
showDebugWindows = False

wht_dice_data = np.zeros(6)
red_dice_data = np.zeros(6)
ylw_dice_data = np.zeros(6)

wht_buffer = []
red_buffer = []
ylw_buffer = []
roll_count = 0
allow_count = True


#Aux Functions
def nothing(x):
    pass

def createTuningTrackbars():
    cv2.namedWindow("Trackbars")
    cv2.createTrackbar("Lower H", "Trackbars", 0, 179, nothing)
    cv2.createTrackbar("Lower S", "Trackbars", 0, 255, nothing)
    cv2.createTrackbar("Lower V", "Trackbars", 0, 255, nothing)
    cv2.createTrackbar("Upper H", "Trackbars", 0, 179, nothing)
    cv2.createTrackbar("Upper S", "Trackbars", 0, 255, nothing)
    cv2.createTrackbar("Upper V", "Trackbars", 0, 255, nothing)

def tunningTest(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lh = cv2.getTrackbarPos("Lower H", "Trackbars")
    ls = cv2.getTrackbarPos("Lower S", "Trackbars")
    lv = cv2.getTrackbarPos("Lower V", "Trackbars")
    uh = cv2.getTrackbarPos("Upper H", "Trackbars")
    us = cv2.getTrackbarPos("Upper S", "Trackbars")
    uv = cv2.getTrackbarPos("Upper V", "Trackbars")
    lower = np.array([lh,ls,lv])
    upper = np.array([uh,us,uv])
    mask = cv2.inRange(hsv, lower, upper)
    cv2.imshow('Test mask', mask)

def dot_detection_mean(buffer):
    buffer_sum = sum(buffer)
    mean = round((buffer_sum/roll_count),0)
    if mean > 6:
        return 6
    else:
        return int(mean)


# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

if showDebugWindows:
    createTuningTrackbars()

while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, None, fx=0.8, fy=0.8, interpolation=cv2.INTER_AREA)

    red_mask = ip.filterRedDice(frame)
    ylw_mask = ip.filterYellowDice(frame)
    wht_mask = ip.filterWhiteDice(frame)

    red_mask = ip.improveImgYlwRed(red_mask)
    ylw_mask = ip.improveImgYlwRed(ylw_mask)
    wht_mask = ip.improveImgWht(wht_mask)

    #Operations in real time frame
    dots_red, red_mask = ip.detectBlobs(red_mask)
    dots_wht, wht_mask = ip.detectBlobs(wht_mask)
    dots_ylw, ylw_mask = ip.detectBlobs(ylw_mask)
    
    #Showing frames
    cv2.imshow('Input', frame)
    if showDebugWindows:
        cv2.imshow('Mask Red', red_mask)
        cv2.imshow('Mask Ylw', ylw_mask)
        cv2.imshow('Mask Wht', wht_mask)
        #tunningTest(frame)

    #Dots counting logic
    #1) Chech if we have dice on screen (any)
    if(dots_red > 0 or dots_wht > 0 or dots_ylw > 0):
        #2) We have dice on screen, so we append dots value to the buffers if roll_count < roll_checks
        if(roll_count < 50):
            red_buffer.append(dots_red)
            wht_buffer.append(dots_wht)
            ylw_buffer.append(dots_ylw)
            roll_count += 1
        elif allow_count:
            #3) Roll count is >= roll_checks, we will now use the mean of the last n roll checks detections to decide how many dots there are in each dice
            mean_red = dot_detection_mean(red_buffer)
            mean_wht = dot_detection_mean(wht_buffer)
            mean_ylw = dot_detection_mean(ylw_buffer)
            #4) Update the number list for each dice
            if(mean_red > 0):
                red_dice_data[mean_red-1] += 1
            if(mean_wht > 0):
                wht_dice_data[mean_wht-1] += 1
            if(mean_ylw > 0):
                ylw_dice_data[mean_ylw-1] += 1
            print('---------------')
            print(f'WHT curr_val: {mean_wht} wht_dice_data: {wht_dice_data}')
            print(f'RED curr_val: {mean_red} red_dice_data: {red_dice_data}')
            print(f'YLW curr_val: {mean_ylw} ylw_dice_data: {ylw_dice_data}')
            allow_count = False #this flag allows counting to be performed only one time each roll
            ui.updateTableValues(window, wht_dice_data, red_dice_data, ylw_dice_data)
            ui.updateLastLaunch(window, mean_wht, mean_red, mean_ylw)
    else:
        #5) If there are no dices on screen, we reset the buffer and the roll count, and allow a new count to be performed
        red_buffer.clear()
        wht_buffer.clear()
        ylw_buffer.clear()
        roll_count = 0
        allow_count = True

    #Wait for window events
    event, values = window.read(timeout=10) #Awaits 10ms for an event
    if event == sg.WIN_CLOSED: #if user closes window
        break
    if event == 'Reset Count':
        ui.clearTableValues(window)
    if event == 'Show/Hide Debug':
        if not showDebugWindows:
            showDebugWindows = True
        else:
            showDebugWindows = False
            cv2.destroyWindow('Mask Red')
            cv2.destroyWindow('Mask Ylw')
            cv2.destroyWindow('Mask Wht')

cap.release()
cv2.destroyAllWindows()


#Autor: Nathan Silva Rodrigues
#Disciplina: PDI - EngComp 2022/02
#Data: Dezembro 2022