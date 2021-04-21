# Gilbert Velasquez
# CS 4375: Theory of Operating Systems
# Dr. Freudenthal
# This file contains the 3 methods required to run Lab Assignment #3's Video Player.

import threading
import cv2
import numpy as np
import queue
import base64
from PCQueue import producerConsumerQueue

# Method given by Dr. Freudenthal to extract frames from a file
def extractFrames(filename,colorFramesQueue,maxFrames):
    count = 0
    vidcap = cv2.VideoCapture(filename)
    success,image = vidcap.read()

    while success and count < maxFrames:
        success,jpgImage = cv2.imencode('.jpeg',image)
        colorFramesQueue.insert(image)
        success,image = vidcap.read()
        count +=1

# Method given by Dr. Freudenthal to convert frames to grayscale
def convertToGrayScale(colorFramesQueue,grayScaleFramesQueue):
    while True:
        if colorFramesQueue.empty():
            continue
        else: 
            frame = colorFramesQueue.remove()
            grayScaleFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            grayScaleFramesQueue.insert(grayScaleFrame)

# Method given by Dr. Freudenthal to display frames
def displayFrames(grayScaleFramesQueue):
    while True:
        frame = grayScaleFramesQueue.remove()
        cv2.imshow('Video',frame)
        if grayScaleFramesQueue.empty():
            continue
        if cv2.waitKey(42) and 0xFF == ord("q"):
            break
        
    cv2.destroyAllWindows()

# Create the Queues
        
colorFramesQueue = producerConsumerQueue()
grayScaleFramesQueue = producerConsumerQueue()
filename = "clip.mp4"

# Create the Threads 

extractFramesThread = threading.Thread(target = extractFrames, args = (filename,colorFramesQueue,9999))

convertToGrayScaleThread = threading.Thread(target = convertToGrayScale, args = (colorFramesQueue,grayScaleFramesQueue))

displayFramesThread = threading.Thread(target = displayFrames, args = {grayScaleFramesQueue})

# Start the Threads

extractFramesThread.start() 
convertToGrayScaleThread.start()
displayFramesThread.start()




