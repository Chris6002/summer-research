import numpy as np
import time
import sys
import os
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2


def createFolder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


createFolder('/media/nvidia/Files/Left')
createFolder('/media/nvidia/Files/Right')
createFolder('/media/nvidia/Files/Center')


def limitValue(n, minn, maxn):
    return max(min(maxn, n), minn)


'''#################  GLOBAL PARAMETER  #################'''
resolution = [640, 480]
record_FPS = 10
speed_range = [1250, 1750]
steer_range = [1000, 1800]
'''#################  CAMERA SETUP  #################'''
'''##############  Realsense  ##############'''
# Configure depth and color streams
import pyrealsense2 as rs
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, resolution[0], resolution[1],
                     rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, resolution[0], resolution[1],
                     rs.format.z16, 30)
# Start streaming
pipeline.start(config)
'''##############  Logitech  ##############'''
cap1 = cv2.VideoCapture(1)
cap1.set(3, resolution[0])
cap1.set(4, resolution[1])
cap2 = cv2.VideoCapture(2)
cap2.set(3, resolution[0])
cap2.set(4, resolution[1])
'''################  SERVO & SERIES  ################'''
'''##############  Polotu  ##############'''
import maestro
servo = maestro.Controller()
import maestro
servo = maestro.Controller('/dev/ttyACM0')
servo.setRange(0, 1000 * 4, 2000 * 4)
servo.setSpeed(0, 35)
servo.setRange(1, 1000 * 4, 2500 * 4)
'''##############  Arduino  ##############'''
import serial
ser = serial.Serial(port='/dev/ttyTHS2', baudrate=115200)  # open serial port
ser.flushInput()
ser.flushOutput()

try:
    starttime = time.time()
    iter_num = 0
    ch3_pre = 0
    while True:
        '''##############  Get command  ##############'''
        command = ser.readline().decode('utf-8').rstrip().split('x')

        ch1 = int(command[0])
        ch2 = int(command[1])
        ch3 = int(command[2])
        if abs(ch3 - ch3_pre) > 500:
            iter_num = iter_num + 1
        '''##############  Get image  ##############'''
        ret, frame1 = cap1.read()
        ret, frame2 = cap2.read()
        real_frames = pipeline.wait_for_frames()
        depth_frame = real_frames.get_depth_frame()
        color_frame = real_frames.get_color_frame()
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        ###!!!!!!!!!Read a line which is terminated with end-of-line (eol) character (\n by default) or until timeout.
        '''##############  SAVE  ##############'''
        #！TODO： 添加folder
        ##################################################################################################################################################
        if ch3 > 1500:
            folder_location = '/media/nvidia/Files/'
            folder_name = 'left/' + str(iter_num)
            if not os.path.exists(folder_location + folder_name):
                os.makedirs(folder_location + folder_name)
            cv2.imwrite('/media/nvidia/Files/1_' + str(i) + '.png', frame1)
            cv2.imwrite('/media/nvidia/Files/1_' + str(i) + '.png', frame1)
            cv2.imwrite('/media/nvidia/Files/1_' + str(i) + '.png', frame1)
        ch3_pre = ch3
        # Convert images to numpy arrays
        '''##############  Send command  ##############'''
        ch1 = limitValue(steer_range[0], steer_range[1])
        ch2 = limitValue(speed_range[0], speed_range[1])
        servo.setTarget(0, ch1 * 4)  #set servo to move to center position
        servo.setTarget(1, ch2 * 4)  #set servo to move to center position
        '''##############  Keep Frequence  ##############'''
        time.sleep(1 / record_FPS - (
            (time.time() - starttime) % (1 / record_FPS)))
finally:

    # Stop streaming
    servo.close()
    ser.close()
    pipeline.stop()
