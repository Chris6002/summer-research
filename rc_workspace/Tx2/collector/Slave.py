import time

# =====================================
# Network Configuration
# =====================================
from multiprocessing.connection import Listener
serv = Listener(('', 25000), authkey=b'peekaboo')


# =====================================
# Camera setup
# =====================================
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
iter_num = 0
try:
    client = serv.accept()
    while True:
        starttime = time.time()
        msg = client.recv().split(':')
        if msg[0] == 'Iter':
            print('creating...')
            if iter_num > 0:
                out1.release()
                out2.release()
            iter_num = msg[1]
            out1 = cv2.VideoWriter(
                '/media/nvidia/Files/Left/' + str(iter_num) + '.avi',
                cv2.VideoWriter_fourcc('X', 'V', 'I', 'D'), 10, (1280, 720))
            out2 = cv2.VideoWriter(
                '/media/nvidia/Files/Right/' + str(iter_num) + '.avi',
                cv2.VideoWriter_fourcc('X', 'V', 'I', 'D'), 10, (1280, 720))
        elif msg[0] == 'Save':
            out1.write(vs1.read())
            out2.write(vs2.read())
        print(time.time() - starttime)
finally:
    out1.release()
    out2.release()
    vs1.stop()
    vs2.stop()