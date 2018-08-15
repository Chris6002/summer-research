import numpy as np
import sys
import time
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2

# =====================================
# Global setting
# =====================================
name='I AM CENTRE'
print(name)
resolution = (640, 480)
record_FPS = 10
frequence = 1 / record_FPS
FourCC = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
folder_path = '/media/nvidia/Files/Centre/'
device = '/dev/v4l/by-id/usb-Intel_R__RealSense_TM__415_Intel_R__RealSense_TM__415_811313022233-video-index0'
port_num = 25002
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
bool_retrieve = cap.grab()
ret, frame = cap.retrieve()
# =====================================
# Init value
# =====================================
start_time = time.time()
end_time = time.time()
iter_num = 0
out = cv2.VideoWriter(folder_path + '0.avi', FourCC, record_FPS,
                      resolution)
index=0
try:
    while True:
        index=index+1
        start_time = time.time()
        msg = client.recv().split(':')
        bool_retrieve = cap.grab()
        previous_frame=frame
        ret, frame = cap.retrieve()
        if bool_retrieve:
            if msg[0] == 'Iter':
                print('creating...')
                if iter_num > 0:
                    out.release()
                iter_num = int(msg[1])
                out = cv2.VideoWriter(folder_path + msg[1]+'.avi', FourCC, record_FPS,
                                    resolution)
            elif msg[0] == 'Save':


                out.write(frame)
                if index>20:
                    index=0
                    print('Saving', end='   ')
                    print(iter_num, end='   ')
                    print(str(round(1/(time.time()-start_time),1)) )
            elif msg[0] == 'Waiting':
                if index>20:
                    index=0
                    print('Waiting', end='   ')
                    print(str(round(1/(time.time()-start_time),1)) )
        else:
            out.write(previous_frame)
            out.write(previous_frame)
            out.write(previous_frame)
            out.write(previous_frame)
            cap.release()
            cap = cv2.VideoCapture(device)
            cap.set(3, resolution[0])
            cap.set(4, resolution[1])
        #if (now - start_time) < frequence:time.sleep(frequence - ((now - start_time) % frequence))
        

finally:
    out.release()
    cap.release()
