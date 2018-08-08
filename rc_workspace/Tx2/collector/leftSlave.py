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
folder_path = '/media/nvidia/Files/Left/'
device = '/dev/v4l/by-id/usb-046d_HD_Webcam_C615_794F2390-video-index0'
port_num = 25000
# =====================================
# Network Configuration
# =====================================
from multiprocessing.connection import Client
client = Client(('localhost', port_num), authkey=b'peekaboo')

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
out = cv2.VideoWriter(folder_path + 'test1.avi', FourCC, record_FPS,
                      resolution)
try:
    while True:

        msg = client.recv().split(':')
        start_time = time.time()
        if msg[0] == 'Iter':
            print('creating...')
            if iter_num > 0:
                out.release()
            iter_num = int(msg[1])
            out = cv2.VideoWriter(folder_path + msg[1], FourCC, record_FPS,
                                  resolution)
        elif msg[0] == 'Save':
            _, frame = cap.read()
            out.write(frame)
            print('Saving', end='   ')
            print(iter_num, end='   ')
            print(1 / (end_time - start_time))
        elif msg[0] == 'Waiting':
            print('Waiting', end='   ')
        if (time.time() - start_time) < (1 / record_FPS):
            time.sleep(1 / record_FPS - (
                (time.time() - start_time) % (1 / record_FPS)))

finally:
    out.release()
    cap.release()