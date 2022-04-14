from http.client import ImproperConnectionState
import queue
import numpy as np
import cv2
import time
import threading
import os

from threading import Thread
from queue import Queue

vidQueueLock = threading.Lock()

videoQueue = Queue(maxsize=0)
frameQueue = Queue(maxsize=0)

videoPath = "./"
framePath = videoPath + "frames/"
os.makedirs(framePath, exist_ok=True)

def captureVideo():
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    count = 1
    vidName = "vid-" + str(count) + ".avi"
    frameRate = 10.0
    out = cv2.VideoWriter(vidName, fourcc, frameRate, (w,h))


    # 0.5 seconds video capture
    duration = 0.5

    print(w, h)

    timeStart = time.time()
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret:
            # has time expired?
            if time.time() - timeStart >= duration:
                count += 1
                oldVidName = vidName
                vidName = "vid-" + str(count) + ".avi"
                timeStart = time.time()
                out = cv2.VideoWriter(vidName, fourcc, frameRate, (w,h))
    
                #lock Video Queue
                videoQueue.put(oldVidName)
            out.write(frame)
    cap.release()
    out.release()
    cv2.destroyAllWindows()

def extractFrame(vidName):
    os.system("ffmpeg -i " + str(videoPath+vidName) + " -r 1 " + str(framePath) + "image-"+"vidName"+".jpeg")
    print("frame extracted")


        
def uploadVideo():
    while True:
        if (videoQueue.empty()):
            time.sleep(1)
        else:
            # extract frames from video
            extractFrame(videoQueue.get())


def uploadFrame():
    pass

thread1 = Thread(target = uploadVideo, args = ())
thread1.start()

captureVideo()




