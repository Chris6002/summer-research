import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
from threading import Thread, Lock
import cv2
import numpy as np
import time
import pyrealsense2 as rs
import os
import subprocess
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 1280, 720,
                     rs.format.bgr8, 30)
pipeline.start(config)
out3 = cv2.VideoWriter('/media/nvidia/Files/'+'test3'+'.avi',cv2.VideoWriter_fourcc('X','V','I','D'), 10, (1280,720))
index=0
subprocess.call('python3 opencv_webcam_multithread.py', shell=True)
try:
    while True :
        starttime = time.time()

        real_frames = pipeline.wait_for_frames()
        #depth_frame = real_frames.get_depth_frame()
        color_frame = real_frames.get_color_frame()
        #depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        out3.write(color_image)
        #frame=np.hstack((frame1, frame2))

        #cv2.imwrite('/media/nvidia/Files/'+str(index)+'.png',frame1)
        index=index+1
        print(time.time() - starttime)

finally:
    # Stop streaming
    out3.release()

