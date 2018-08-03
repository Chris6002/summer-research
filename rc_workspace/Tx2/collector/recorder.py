import numpy as np
import time
import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2
'''#################  GLOBAL PARAMETER  #################'''
resolution = [640, 480]
record_FPS = 10
'''#################  CAMERA SETUP  #################'''
'''##############  Realsense  ##############'''
# Configure depth and color streams
import pyrealsense2 as rs
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, resolution[0], resolution[1],
                     rs.format.bgr8, 30)
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
    while True:
        '''##############  Get command  ##############'''
        command = ser.readline().decode('utf-8').rstrip().split('x')
        ch1 = int(command[0])
        ch2 = int(command[1])
        ch3 = int(command[2])
        '''##############  Get image  ##############'''
        ret, frame1 = cap1.read()
        ret, frame2 = cap2.read()
        frames3 = pipeline.wait_for_frames()
        color_frame3 = frames3.get_color_frame()
        color_image = np.asanyarray(color_frame3.get_data())
        ###!!!!!!!!!Read a line which is terminated with end-of-line (eol) character (\n by default) or until timeout.
        '''##############  SAVE  ##############'''
        #！TODO： 添加folder
        cv2.imwrite('/media/nvidia/Files/1_' + str(i) + '.png', frame1)
        cv2.imwrite('/media/nvidia/Files/1_' + str(i) + '.png', frame1)
        cv2.imwrite('/media/nvidia/Files/1_' + str(i) + '.png', frame1)
        # Convert images to numpy arrays
        '''##############  Send command  ##############'''
        servo.setTarget(0, ch1)  #set servo to move to center position
        servo.setTarget(1, ch2)  #set servo to move to center position
        servo.setTarget(2, ch3)  #set servo to move to center position
        servo.setTarget(3, ch4)  #set servo to move to center position
        '''##############  Keep Frequence  ##############'''
        time.sleep(1 / record_FPS - (
            (time.time() - starttime) % (1 / record_FPS)))
finally:

    # Stop streaming
    servo.close()
    ser.close()
    pipeline.stop()
