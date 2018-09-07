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
parser.add_argument('--verify', type=int, default=0)
parser.add_argument('--Dagger', type=int, default=0)
parser.add_argument('--iter', type=int)
args = parser.parse_args()
for arg in vars(args):
    print("Argu: {:>16}:{:<10}".format(arg, getattr(args, arg)))
print('Loading parameter')
monitor = Monitor(args.parameter)
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
ch1_pre = 1476
flag = 0
detech1 = 1
situation = 0
adjust_flag = 1
frame_index = 0
buffer_length = 10
adjust = 0
count = 0
save=0
frame_index = 0
ch1, ch2, ch3 = 1476, 1500, 976
steer_queue = []
# =====================================
# CSV
# =====================================
FourCC = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')

Command_file = '/media/nvidia/Files/Dagger/'
createFolder(Command_file)
import csv
now=time.strftime("%d_%m_%H_%M_%S")
# Dagger command file:
f = open(Command_file + 'Dagger_'+str(args.iter)+'_command'+now+'.csv', 'w')
fnames = ['name','frame', 'steering', 'speed', 'category', 'stage']
writer = csv.DictWriter(f, fieldnames=fnames)
writer.writeheader()
# verify time file:
time_file = open(Command_file + 'Time_'+str(args.iter)+now+'.csv', 'w')
time_fnames = ['end_frame', 'time']
time_writer = csv.DictWriter(time_file, fieldnames=time_fnames)


out = cv2.VideoWriter(Command_file + 'Dagger_'+str(args.iter)+now+'.avi', FourCC, 10,
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
start_time = time.time()
time_without_intervention = 0
time_auto_start = 0
try:
    while True:
        # ======  Get command  ====== #
        try:
            
            command = ser.readline().decode('utf-8').rstrip().split('x')
            try:
                ch1, ch2, ch3, ch4 = int(command[0].strip('\x00')), int(command[1].strip(
                    '\x00')), int(command[2].strip('\x00')), int(command[3].strip('\x00'))
                ch1_real = ch1
                #print(ch1,ch2,ch3,ch4)
            except:
                ch1, ch2, ch3, ch4 = 1476, 1500, 976, 1960
                
                ch1_real = ch1
            dis = ch3-ch3_pre
            dis4 = ch4-ch4_pre

            if dis > 500 and situation == 0:
                situation = 1
            elif dis < -500 and situation == 1:
                situation, flag = 0, 0

            if abs(dis4) > 500:
                adjust_flag = 0 if adjust_flag == 1 else 1

                if adjust_flag:
                    if args.verify==1:
                        time_without_intervention = time.time()-time_auto_start
                        print('Manual Now verify auto ends: ',time_without_intervention)
                        if save:
                            print('verify save')
                            data = {'end_frame': 1, 'time': round(time_without_intervention, 3)}
                            time_writer.writerow(data)
                    elif args.Dagger==1:
                        print('Manual Now Dagger auto ends: ',time_without_intervention)
                else:
                    print('auto start',end=' ')
                    if args.verify == 1:
                        print('verify')
                        time_auto_start = time.time()
                    if args.Dagger==1:
                        print('Dagger')
            if adjust_flag == 0:
                if abs(ch1_real-1500) > 50:
                    adjust_flag = 1
                    if adjust_flag:
                        print('Manual Now')
                        if args.verify == 1:

                            time_without_intervention = time.time()-time_auto_start
                            print('verify auto ends: ',
                                  time_without_intervention)
                            if save:
                                print('verify save')
                                data = {'end_frame': 1, 'time': round(time_without_intervention, 3)}
                                time_writer.writerow(data)
                        elif args.Dagger==1:
                            print('Manual Now Dagger auto ends: ',time_without_intervention)
                    else:
                        print('auto start',end=' ')
                        if args.verify == 1:
                            print('verify')
                            time_auto_start = time.time()
                        if args.Dagger==1:
                            print('Dagger')
            bool_retrieve = cap.grab()
            ret, frame = cap.retrieve()

            if bool_retrieve:
                if adjust_flag == 0:
                    ch1 = monitor.inference(frame).item()

                else:
                    ch1 = ch1_real
            else:
                cap.release()
                cap = cv2.VideoCapture(device)
                cap.set(3, resolution[0])
                cap.set(4, resolution[1])
            if ch3 > 1900:
                save=1
                if time.time()-start_time > 0.1:

                    if args.Dagger == 1:
                        print('Dagger save')
                        out.write(frame)
                        frame_index += 1
                        data = {'name':args.iter,'frame': frame_index, 'steering': ch1,
                                'speed': ch2, 'category': 0, 'stage': adjust_flag}
                        writer.writerow(data)
                        start_time = time.time()
            else: save=0


        except UnicodeDecodeError:
            ch1, ch2, ch3 = 1476, 1500, 976
            print('hehe')

        # ======  Send command  ====== #
        ch1 = limitValue(ch1, steer_range[0], steer_range[1])
        ch2 = limitValue(ch2, speed_range[0], speed_range[1])
        servo.setTarget(0, ch1 * 4)  # set servo to move to centre position
        servo.setTarget(1, ch2 * 4)  # set servo to move to centre position
        # ============================ #
        ch3_pre = ch3
        ch4_pre = ch4
        ch1_pre = ch1_real
finally:
    servo.setTarget(0, 1476 * 4)  # set servo to move to centre position
    servo.setTarget(1, 1500 * 4)  # set servo to move to centre position
    servo.close()
    ser.close()
    f.close()
    time_file.close()
    print('finished')
