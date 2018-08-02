import numpy as np
import sys
import time
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2




#640,480
resolution=[640,480]
record_FPS=10

import pyrealsense2 as rs
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, resolution[0], resolution[1], rs.format.bgr8, 30)
# Start streaming
pipeline.start(config)






cap1 = cv2.VideoCapture(1)
cap1.set(3,resolution[0])
cap1.set(4,resolution[1])
cap2 = cv2.VideoCapture(2)
cap2.set(3,resolution[0])
cap2.set(4,resolution[1])
i=0
while(True):
    starttime=time.time()
    # Capture frame-by-frame
    ret, frame1 = cap1.read()
    ret, frame2 = cap2.read()
    frames3 = pipeline.wait_for_frames()
    color_frame3 = frames3.get_color_frame()
    color_image = np.asanyarray(color_frame3.get_data())
    i=i+1
    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imwrite('/media/nvidia/Files/1_'+str(i)+'.png',frame1)
    #cv2.imwrite('/media/nvidia/Files/2_'+str(i)+'.png',frame2)
    images=np.hstack((frame1, color_image,frame2))
    cv2.imshow('frame3',images)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    time.sleep(1/record_FPS-((time.time() - starttime) % (1/record_FPS)))

# When everything done, release the capture
cap1.release()
cv2.destroyAllWindows()
