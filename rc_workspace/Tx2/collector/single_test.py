import numpy as np
import sys
import time
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2

# =====================================
# Global setting
# =====================================
resolution = (1280, 720)
record_FPS = 10
FourCC = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
folder_path = '/media/nvidia/Files/Right/'
device = '/dev/v4l/by-id/usb-046d_HD_Webcam_C615_06D65490-video-index0'
port_num = 25001

# =====================================
# Camera setup
# =====================================
cap = cv2.VideoCapture(device)
cap.set(3, resolution[0])
cap.set(4, resolution[1])

# =====================================
# Init value
# =====================================
start_time = time.time()
end_time = time.time()
iter_num = 0
out = cv2.VideoWriter('/media/nvidia/Files/test.avi', FourCC, record_FPS,
                      resolution)
try:
    while True:
        start_time=time.time()
        _, frame = cap.read()
        out.write(frame)
        print(str(round(1/(time.time() - start_time),1)))

finally:
    out.release()
    cap.release()
