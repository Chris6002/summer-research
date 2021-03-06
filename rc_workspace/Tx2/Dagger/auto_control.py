import time
import os
import numpy as np
from director import Monitor
import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--parameter', type=str)
args = parser.parse_args()
for arg in vars(args):
    print("Argu: {:>16}:{:<10}".format(arg, getattr(args, arg)))
print('Loading parameter')
monitor=Monitor(args.parameter)
print('Finish loading')
# =====================================
# Convenient function
# =====================================

def createFolder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
def limitValue(n, minn, maxn):
    return max(min(maxn, n), minn)

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
# Init value
# =====================================
resolution = (640, 480)
device = '/dev/v4l/by-id/usb-Intel_R__RealSense_TM__415_Intel_R__RealSense_TM__415_811313022233-video-index0'
start_time = time.time()
end_time = time.time()
iter_num = 0
speed_range = [1250, 1750]
steer_range = [976, 1976]
ch3_pre = 1000
ch4_pre = 1960
flag=0
situation=0
# 0=auto 1=manually
adjust_flag=1
frame_index=0
buffer_length=10
adjust=0
count=0
frame_index=0
ch1, ch2, ch3=1476,1500,976
steer_queue=[]
# =====================================
# CSV
# =====================================
FourCC = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')

Command_file='/media/nvidia/Files/audo_test/'
createFolder(Command_file)
import csv
f = open(Command_file+ '0_command.csv', 'w')
time_file=open(Command_file+ 'time.csv', 'w')
fnames = ['frame', 'steering', 'speed', 'category','stage']
time_fnames=['end_frame','time']
time_writer=csv.DictWriter(time_file,fieldnames=time_fnames)
writer = csv.DictWriter(f, fieldnames=fnames)
time_writer.writeheader()
writer.writeheader()

out = cv2.VideoWriter(Command_file + '0.avi', FourCC, 10,
                      resolution)
# =====================================
# Camera setup
# =====================================
cap = cv2.VideoCapture(device)
cap.set(3, resolution[0])
cap.set(4, resolution[1])
bool_retrieve = cap.grab()
ret, frame = cap.retrieve()
print('camera done')
start_time=time.time()
time_without_intervention=time.time()
try:
    while True:
        # ======  Get command  ====== #
        try:
            
            
            command =ser.readline().decode('utf-8').rstrip().split('x')
            try:
                ch1, ch2, ch3,ch4 = int(command[0].strip('\x00')), int(command[1].strip('\x00')), int(command[2].strip('\x00')),int(command[3].strip('\x00'))
                ch1_real=ch1
            except:
                ch1, ch2, ch3,ch4=1476,1500,976  ,1960      
            dis=ch3-ch3_pre
            dis4=ch4-ch4_pre
            if dis>500 and situation==0:situation=1
            elif dis<-500 and situation==1:situation,flag=0,0
            if abs(dis4) >500 :
                adjust_flag=0 if adjust_flag==1 else 1
                if adjust_flag:
                    duration=time.time()-time_without_intervention
                    print(duration)
                    data = {'end_frame': 1, 'time':round(duration,3)}
                    time_writer.writerow(data)
                    print('Manual Now')
                else:
                    time_without_intervention=time.time()
                    print(time_without_intervention)
                    print('Auto Now')
            bool_retrieve = cap.grab()
            ret, frame = cap.retrieve()
            
  
            if bool_retrieve:
                if adjust_flag==0:
                    ch1=monitor.inference(frame).item()
                    #print(ch1)
                else:
                    ch1=ch1_real 
       
            else:
                cap.release()
                cap = cv2.VideoCapture(device)
                cap.set(3, resolution[0])
                cap.set(4, resolution[1])
            if ch3>1500 and adjust_flag==0:
                if time.time()-start_time>0.1:
                    print('save')
                    out.write(frame)
                    frame_index+=1
                    data = {'frame': frame_index,'steering': ch1,'speed': ch2,'category': 0, 'stage':adjust_flag}
                    writer.writerow(data)
                    start_time=time.time() 
            
        except UnicodeDecodeError:
            ch1, ch2, ch3=1476,1500,976
            print('hehe')

        # ======  Send command  ====== #
        ch1 = limitValue(ch1, steer_range[0], steer_range[1])
        ch2 = limitValue(ch2, speed_range[0], speed_range[1])
        servo.setTarget(0, ch1 * 4)  #set servo to move to centre position
        servo.setTarget(1, ch2 * 4)  #set servo to move to centre position
        # ============================ #
        ch3_pre = ch3
        ch4_pre = ch4
finally:
    servo.setTarget(0, 1476 * 4)  #set servo to move to centre position
    servo.setTarget(1, 1500 * 4)  #set servo to move to centre position
    servo.close()
    ser.close()
    time_file.close()
    print('finished')
