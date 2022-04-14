import numpy as np
import cv2
import time

from threading import Thread

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
                vidName = "vid-" + str(count) + ".avi"
                timeStart = time.time()
                out = cv2.VideoWriter(vidName, fourcc, frameRate, (w,h))
            out.write(frame)
    cap.release()
    out.release()
    cv2.destroyAllWindows()

captureVideo()


