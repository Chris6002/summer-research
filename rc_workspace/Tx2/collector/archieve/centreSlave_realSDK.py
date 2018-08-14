import time
import sys
import os
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2
import numpy as np
# =====================================
# Global setting
# =====================================
folder_path =  '/media/nvidia/Files/Centre/'

resolution = (640,480)
record_FPS = 10
frequence = 1 / record_FPS
FourCC = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
port_num=25002

# =====================================
# Network Configuration
# =====================================
from multiprocessing.connection import Client
client = Client(('localhost', port_num), authkey=b'peekaboo')


# =====================================
# Camera setup
# =====================================
import pyrealsense2 as rs
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, resolution[0], resolution[1],
                     rs.format.bgr8, 30)

pipeline.start(config)

# =====================================
# Init value
# =====================================
out = cv2.VideoWriter(folder_path + '0.avi', FourCC, record_FPS,
                      resolution)
start_time = time.time()
end_time = time.time()
iter_num = 0
try:
    while True:
        start_time = time.time()
        msg = client.recv().split(':')
        real_frames = pipeline.wait_for_frames()
        color_image = np.asanyarray((real_frames.get_color_frame().get_data()))
        if msg[0] == 'Iter':
            print('creating...')
            if iter_num > 0:
                out.release()
            iter_num = int(msg[1])
            out = cv2.VideoWriter(folder_path + msg[1]+'.avi', FourCC, record_FPS,
                                  resolution)
        elif msg[0] == 'Save':

            out.write(color_image)
            print('Saving', end='   ')
            print(iter_num, end='   ')
        elif msg[0] == 'Waiting':
            print('Waiting', end='   ')
        now=time.time()
        #if (now - start_time) < frequence:time.sleep(frequence - ((now - start_time) % frequence))
        print(str(round(1/(time.time()-start_time),1)) )

finally:
    out.release()
    pipeline.stop()
    print('finished')
