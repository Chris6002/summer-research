import time
import sys
import os
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2
import numpy as np
# =====================================
# Network Configuration
# =====================================

from multiprocessing.connection import Client
c = Client(('localhost', 25000), authkey=b'peekaboo')
# =====================================
# Global setting
# =====================================
camera_left = '/media/nvidia/Files/Left/'
camera_right = '/media/nvidia/Files/Right/'
camera_center = '/media/nvidia/Files/Center/'
resolution = [1280, 720]
record_FPS = 10
speed_range = [1400, 1750]
steer_range = [1000, 1800]


# =====================================
# Convenient function
# =====================================
def createFolder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


def limitValue(n, minn, maxn):
    return max(min(maxn, n), minn)


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
createFolder('/media/nvidia/Files/Left')
createFolder('/media/nvidia/Files/Right')
createFolder('/media/nvidia/Files/Center')
f = open('/media/nvidia/Files/data_c.csv', 'w')
fnames = ['name', 'steering', 'speed', 'category']
writer = csv.DictWriter(f, fieldnames=fnames)
writer.writeheader()

# =====================================
# Main Function
# =====================================
try:
    iter_num = 0
    ch3_pre = 0
    while True:
        starttime = time.time()
        # ======  Get command  ====== #
        ser.flushInput()
        command = ser.readline().decode('utf-8').rstrip().split('x')
        ch1, ch2, ch3 = int(command[0]), int(command[1]), int(command[2])
        # =========================== #
        if ch3 - ch3_pre > 100:
        	c.send('Iter:' + str(iter_num))
        	
        	print(iter_num)
        	out = cv2.VideoWriter('/media/nvidia/Files/Center/' + str(iter_num) + '.avi',cv2.VideoWriter_fourcc('X', 'V', 'I', 'D'), 10,(resolution[0], resolution[1]))
        	iter_num = iter_num + 1
        if ch3_pre > 1500:
            # ======  Get Image  ====== #
            real_frames = pipeline.wait_for_frames()
            color_frame = real_frames.get_color_frame()
            color_image = np.asanyarray(color_frame.get_data())
            # ========================= #
            data = {
                'name': iter_num,
                'steering': ch1,
                'speed': ch2,
                'category': 0
            }
            # ======  Save  ====== #
            print('saving',end="   ")
            
            c.send('Save')
            out.write(color_image)
            writer.writerow(data)
            # ==================== #
        else:
        	c.send('Waiting')
        	print('Waiting',end='   ')
        # ======  Send command  ====== #
        ch1 = limitValue(ch1, steer_range[0], steer_range[1])
        ch2 = limitValue(ch2, speed_range[0], speed_range[1])
        servo.setTarget(0, ch1 * 4)  #set servo to move to center position
        servo.setTarget(1, ch2 * 4)  #set servo to move to center position
        # ============================ #
        if round(1/(time.time() - starttime),2)>record_FPS+1:
        	time.sleep(1 / record_FPS - (
            	(time.time() - starttime) % (1 / record_FPS)))
        print(str(round(1/(time.time() - starttime),2)))
        ch3_pre=ch3

        

finally:
    print('finished')
