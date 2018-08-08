import time
import sys
import os
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2
import numpy as np


# =====================================
# Global setting
# =====================================
camera_left = '/media/nvidia/Files/Left/'
camera_right = '/media/nvidia/Files/Right/'
camera_center = '/media/nvidia/Files/Center/'
resolution = (1280, 720)
record_FPS = 10
frequence = 1 / record_FPS
speed_range = [1250, 1750]
steer_range = [976, 1976]
FourCC = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')


# =====================================
# Convenient function
# =====================================
def createFolder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


def getCommand(line):
    command = line.decode('utf-8').rstrip().split('x')
    ch1, ch2, ch3 = int(command[0]), int(command[1]), int(command[2])
    return ch1, ch2, ch3


def limitValue(n, minn, maxn):
    return max(min(maxn, n), minn)
# =====================================
# Network Configuration
# =====================================
from multiprocessing.connection import Listener
print('Left first, right after')
server4left = Listener(('', 25000), authkey=b'peekaboo').accept()
print('Connected to left')
server4right = Listener(('', 25001), authkey=b'peekaboo').accept()
print('Connected to left')
createFolder('/media/nvidia/Files/Left')
createFolder('/media/nvidia/Files/Right')
createFolder('/media/nvidia/Files/Center')
# =====================================
# Camera setup
# =====================================
import pyrealsense2 as rs
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, resolution[0], resolution[1],
                     rs.format.bgr8, 30)
#config.enable_stream(rs.stream.depth, resolution[0], resolution[1],
#                     rs.format.z16, 30)
# Start streaming
pipeline.start(config)
# =====================================
# SERVO & SERIES
# =====================================
#  Polotu
import maestro
servo = maestro.Controller()
import maestro
servo = maestro.Controller('/dev/ttyACM0')
servo.setRange(0, 1000 * 4, 2000 * 4)
servo.setSpeed(0, 45)
servo.setRange(1, 1000 * 4, 2500 * 4)
#  Arduino
import serial
ser = serial.Serial(port='/dev/ttyTHS2', baudrate=115200)  # open serial port
ser.flushInput()
ser.flushOutput()
# =====================================
# CSV
# =====================================
import csv
f = open('/media/nvidia/Files/data_c.csv', 'w')
fnames = ['name', 'steering', 'speed', 'category']
writer = csv.DictWriter(f, fieldnames=fnames)
writer.writeheader()
# =====================================
# Init value
# =====================================

start_time = time.time()
end_time = time.time()
iter_num = 0
ch3_pre = 1000
flag=0
situation=0
try:
    while True:
        end_time = time.time()
        # ======  Get command  ====== #
        ser.flushInput()
        ch1, ch2, ch3 = getCommand(ser.readline())
        dis=ch3-ch3_pre
        if dis>500 and situation==0:
            situation=1
        elif dis<-500 and situation==1:
            situation=0 
            flag=0

        # =========  END  =========== #

        # ========  New file   ====== #
        if situation==1 and flag==0:
            flag=1
            print('enter')
            iter_num = iter_num + 1
            server4left.send('Iter:' + str(iter_num))
            server4right.send('Iter:' + str(iter_num))
            time.sleep(0.1)
            out = cv2.VideoWriter(camera_center + str(iter_num) + '.avi',
                                  FourCC, record_FPS, resolution)
            

        # ==========  END  ========= #
        # ========  Get + Save data  ======== #
        if ch3_pre > 1500 and flag==1:
            
            # =========  Get  ========== #
            real_frames = pipeline.wait_for_frames()
            color_image = np.asanyarray(
                (real_frames.get_color_frame().get_data()))
            data = {
                'name': iter_num,
                'steering': ch1,
                'speed': ch2,
                'category': 0
            }
            # =========  Save  ========== #

            server4left.send('Save')
            server4right.send('Save')

#               print('saving   '+ str(iter_num), end="   ")
            out.write(color_image)
            writer.writerow(data)
        # ===============  END  ============== #

        else:
            server4left.send('Waiting')
            server4right.send('Waiting')
#              print('Waiting', end='   ')
#          print(str(round(1 / (time.time() - end_time), 2)))
        
        # ======  Send command  ====== #
        ch1 = limitValue(ch1, steer_range[0], steer_range[1])
        ch2 = limitValue(ch2, speed_range[0], speed_range[1])
        servo.setTarget(0, ch1 * 4)  #set servo to move to center position
        servo.setTarget(1, ch2 * 4)  #set servo to move to center position
        # ============================ #
        now = time.time()
        if (now - end_time) < frequence:time.sleep(frequence - ((now - start_time) % frequence))
        print(str(round(1/(time.time()-end_time),1)))
        ch3_pre = ch3

finally:
    f.close()
    out.release()
    servo.close()
    ser.close()
    pipeline.stop()
    print('finished')
