#!/usr/bin/env python
import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
from threading import Thread, Lock
import cv2
import numpy as np
import time
import pyrealsense2 as rs
#pipeline = rs.pipeline()
#config = rs.config()
#config.enable_stream(rs.stream.color, 1280, 720,rs.format.bgr8, 30)
#pipeline.start(config)
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
            time.sleep(1 / 10)

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
   
    out1 = cv2.VideoWriter('/media/nvidia/Files/'+'test1'+'.avi',cv2.VideoWriter_fourcc('X','V','I','D'), 10, (1280,720))

starttime = time.time()
endtime = time.time()

try:
    while True :
        endtime = time.time()
        if endtime-starttime > 0.1:
            frame1 = vs1.read()

            #images=np.hstack((frame1,frame2))
            #real_frames = pipeline.wait_for_frames()
            #depth_frame = real_frames.get_depth_frame()
            #color_frame = real_frames.get_color_frame()
            #depth_image = np.asanyarray(depth_frame.get_data())
            #color_image = np.asanyarray(color_frame.get_data())
            #cv2.imshow('frame3',images)
            #if cv2.waitKey(1) & 0xFF == ord('q'):
            #    break

            out1.write(frame1)
            #out3.write(color_image)
            #frame=np.hstack((frame1, frame2))

            #cv2.imwrite('/media/nvidia/Files/'+str(index)+'.png',frame1)
            print(time.time() - starttime)
            starttime = time.time()

finally:
    # Stop streaming
    out1.release()
    out2.release()
    vs1.stop()
    vs2.stop()
    cv2.destroyAllWindows()
