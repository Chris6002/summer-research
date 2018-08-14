import time
import sys
import os
from threading import Thread, Lock
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2
import numpy as np
record_FPS = 10
# =====================================
# Network Configuration
# =====================================
from multiprocessing.connection import Listener


def createFolder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


createFolder('/media/nvidia/Files/Left')
createFolder('/media/nvidia/Files/Right')
createFolder('/media/nvidia/Files/Center')
# =====================================
# Camera setup
# =====================================


class ClientStream:
    def __init__(self,server):
        self.server =server
        self.started = False
        self.read_lock = Lock()
        self.msg=['init']
    def start(self):
    
        self.client=self.server.accept()
        print("started!!")
        if self.started:
            print("already started!!")
            return None
        self.started = True
        self.thread = Thread(target=self.update, args=()).start()
        
        return self

    def update(self):
        while self.started:
            msg = self.client.recv().split(':')
            self.read_lock.acquire()
            self.msg = msg
            self.read_lock.release()


    def read(self):
        self.read_lock.acquire()
        msg = self.msg.copy()
        self.read_lock.release()
        return msg

    def stop(self):
        self.started = False
        self.thread.join()


class WebcamVideoStream:
    def __init__(self, src=0, width=1280, height=720):
        self.stream = cv2.VideoCapture(src)
        self.stream.set(3, width)
        self.stream.set(4, height)
        (self.grabbed, self.frame) = self.stream.read()
        self.started = False
        self.read_lock = Lock()

    def start(self):
        if self.started:
            print("already started!!")
            return None
        self.started = True
        self.thread = Thread(target=self.update, args=())
        self.thread.start()

        return self

    def update(self):
        while self.started:
            (grabbed, frame) = self.stream.read()
            self.read_lock.acquire()
            self.grabbed, self.frame = grabbed, frame
            self.read_lock.release()

    def read(self):
        self.read_lock.acquire()
        frame = self.frame.copy()
        self.read_lock.release()
        return frame

    def stop(self):
        self.started = False
        self.thread.join()

    def __exit__(self, exc_type, exc_value, traceback):
        self.stream.release()


vs1 = WebcamVideoStream(
    '/dev/v4l/by-id/usb-046d_HD_Webcam_C615_794F2390-video-index0').start()
vs2 = WebcamVideoStream(
    '/dev/v4l/by-id/usb-046d_HD_Webcam_C615_06D65490-video-index0').start()
out1 = cv2.VideoWriter('/media/nvidia/Files/Left/' + '0.avi',
                       cv2.VideoWriter_fourcc('X', 'V', 'I', 'D'), 10,
                       (1280, 720))
out2 = cv2.VideoWriter('/media/nvidia/Files/Right/' + '0.avi',
                       cv2.VideoWriter_fourcc('X', 'V', 'I', 'D'), 10,
                       (1280, 720))
client = ClientStream(Listener(('', 25000), authkey=b'peekaboo')).start()

iter_num = 0
starttime = time.time()
endtime = time.time()
iter_num=0
msg_pre=['init']
try:
    while True:
        endtime = time.time()
        if endtime-starttime > 0.1:

            msg = client.read()

            if msg != msg_pre:
                iter_num=iter_num+1
                print('creating...')
                if iter_num > 0:
                    out1.release()
                    out2.release()
                print(iter_num)
                out1 = cv2.VideoWriter(
                    '/media/nvidia/Files/Left/' + str(iter_num) + '.avi',
                    cv2.VideoWriter_fourcc('X', 'V', 'I', 'D'), 10, (1280, 720))
                out2 = cv2.VideoWriter(
                    '/media/nvidia/Files/Right/' + str(iter_num) + '.avi',
                    cv2.VideoWriter_fourcc('X', 'V', 'I', 'D'), 10, (1280, 720))
            elif msg[0] == 'Save':
                    out1.write(vs1.read())
                    out2.write(vs2.read())
                    #frame1,frame2 = vs1.read(),vs2.read()
                    #cv2.imshow('frame3',np.hstack((frame1,frame2)))
                    #if cv2.waitKey(30) & 0xFF == ord('q'):break
                    print('Saving', end='   ')
                    print(iter_num, end='   ')
                    print(1/(endtime-starttime))
                    
            
            elif msg[0] == 'Waiting':
                print('Waiting')
            msg_pre=msg
            starttime = time.time()
finally:
    out1.release()
    out2.release()
    vs1.stop()
    vs1.__exit__()
    vs2.stop()
    vs2.__exit__()
