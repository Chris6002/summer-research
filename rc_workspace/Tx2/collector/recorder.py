import pyrealsense2 as rs
import numpy as np
import time
import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2
'''
##################################################
#################  CAMERA SETUP  #################
##################################################
'''
'''##############  Realsense  ##############'''
# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
# Start streaming
pipeline.start(config)
'''##############  Logitech  ##############'''

'''
##################################################
################  SERVO & SERIES  ################
##################################################
'''
'''##############  Polotu  ##############'''
import maestro
servo = maestro.Controller()
'''##############  Arduino  ##############'''
import serial
ser=serial.Serial('/dev/ttyTHS2')  # open serial port



servo.setAccel(0,4)      #set servo 0 acceleration to 4
servo.setTarget(0,6000)  #set servo to move to center position
servo.setSpeed(1,10)     #set speed of servo 1
x = servo.getPosition(1) #get the current position of servo 1


record_FPS=10
try:
    starttime=time.time()
    while True:

        '''##############  Get image  ##############'''
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        '''##############  Get command  ##############'''
        command = ser.readline()
        '''!TODO:
        ch1=command[xxx]
        ch2=command[xxx]
        ch3=command[xxx]
        ch4=command[xxx]
        '''
        ###!!!!!!!!!Read a line which is terminated with end-of-line (eol) character (\n by default) or until timeout.
        
        '''##############  SAVE  ##############'''


        # Convert images to numpy arrays

        color_image = np.asanyarray(color_frame.get_data())


        # Stack both images horizontally
        images =color_image
        #print('hehe')
        # Show images
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', images)
        cv2.waitKey(1)
        


        '''##############  Send command  ##############'''
        servo.setTarget(0,ch1)  #set servo to move to center position
        servo.setTarget(1,ch2)  #set servo to move to center position
        servo.setTarget(2,ch3)  #set servo to move to center position
        servo.setTarget(3,ch4)  #set servo to move to center position
        '''##############  Keep Frequence  ##############'''
        time.sleep(1/record_FPS-((time.time() - starttime) % (1/record_FPS)))
finally:

    # Stop streaming
    servo.close()
    ser.close()
    pipeline.stop()
