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


#vidName naming convetntion : vid-<COUNT>.avi
#FrameName can be: frame-vid<count>-<count>.avi
def extractFrame(vidName):
    frameName = vidName[:-4]
    print (frameName)
    frameName = "frame-"+frameName+"-%3d.jpeg"
    print(frameName)
    absFramePath = str(framePath)+frameName

    # png format seems to be consuming lots of disk space. Need to decide later if it is better for face recognition
    os.system("ffmpeg -i " + str(videoPath+vidName) + " -r 2 " + absFramePath)
    print("frame extracted")
    addFrameToQueue(vidName)

#for the specific video add the related frames in the queue
def addFrameToQueue(vidName):
    #converting vidName to uniquely identify its associated frames
    vidName = vidName[:-4]
    searchString = "-"+vidName+"-"

    for fileName in os.listdir(framePath):
        if (fileName.endswith(".jpeg")):
            if searchString in fileName:
                absFramePath = framePath + fileName
                print("absolute frame path " + absFramePath)
                frameQueue.put(absFramePath)
    


    

    

# extract frame 
# upload the frame in s3
# upload the video in s3        
def uploadVideo():
    while True:
        if (videoQueue.empty()):
            time.sleep(1)
        else:
            # extract frames from video
            extractFrame(videoQueue.get())



# get all the frames from 
def uploadFrame():
    pass


# collect response from SQS
# process the result and dump
def collectResult():
    pass

thread1 = Thread(target = uploadVideo, args = ())
thread1.start()

captureVideo()




