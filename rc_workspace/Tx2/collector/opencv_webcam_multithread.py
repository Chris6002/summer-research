#!/usr/bin/env python
import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
from threading import Thread, Lock
import cv2
import numpy as np
import time
class WebcamVideoStream :
    def __init__(self, src = 0, width = 1280, height = 720) :
        self.stream = cv2.VideoCapture(src)
        self.stream.set(3, width)
        self.stream.set(4, height)
        (self.grabbed, self.frame) = self.stream.read()
        self.started = False
        self.read_lock = Lock()

    def start(self) :
        if self.started :
            print ("already started!!")
            return None
        self.started = True
        self.thread = Thread(target=self.update, args=())
        self.thread.start()
        return self

    def update(self) :
        while self.started :
            (grabbed, frame) = self.stream.read()
            self.read_lock.acquire()
            self.grabbed, self.frame = grabbed, frame
            self.read_lock.release()

    def read(self) :
        self.read_lock.acquire()
        frame = self.frame.copy()
        self.read_lock.release()
        return frame

    def stop(self) :
        self.started = False
        self.thread.join()

    def __exit__(self, exc_type, exc_value, traceback) :
        self.stream.release()

if __name__ == "__main__" :
    vs1 = WebcamVideoStream('/dev/v4l/by-id/usb-046d_HD_Webcam_C615_794F2390-video-index0').start()
    vs2 = WebcamVideoStream('/dev/v4l/by-id/usb-046d_HD_Webcam_C615_06D65490-video-index0').start()
    index=0    
    while True :
        starttime = time.time()
        frame1 = vs1.read()
        frame2 = vs2.read()
        frame=np.hstack((frame1, frame2))

        cv2.imwrite('/media/nvidia/Files/'+str(index)+'.png',frame1)
        index=index+1
        print(time.time() - starttime)
    vs1.stop()
    vs2.stop()
    cv2.destroyAllWindows()
