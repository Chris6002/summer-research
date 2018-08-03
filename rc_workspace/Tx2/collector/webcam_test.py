import numpy as np
import sys
import time
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2

#640,480
resolution=[1280,720]
record_FPS=10

cap1 = cv2.VideoCapture('/dev/v4l/by-id/usb-046d_HD_Webcam_C615_06D65490-video-index0')
cap1.set(3,resolution[0])
cap1.set(4,resolution[1])
cap2 = cv2.VideoCapture('/dev/v4l/by-id/usb-046d_HD_Webcam_C615_794F2390-video-index0')
cap2.set(3,resolution[0])
cap2.set(4,resolution[1])

while(True):
    starttime=time.time()
    # Capture frame-by-frame
    ret, frame1 = cap1.read()
    ret, frame2 = cap2.read()
    images=np.hstack((frame1,frame2))
    cv2.imshow('frame3',images)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    time.sleep(1/record_FPS-((time.time() - starttime) % (1/record_FPS)))
