import numpy as np
import sys
import time
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2




#640,480
resolution=[1280,720]
record_FPS=10

device_name1='/dev/v4l/by-id/usb-046d_HD_Webcam_C615_06D65490-video-index0'
device_name2='/dev/v4l/by-id/usb-046d_HD_Webcam_C615_794F2390-video-index0'
device_name3='/dev/v4l/by-id/usb-Intel_R__RealSense_TM__415_Intel_R__RealSense_TM__415_811313022233-video-index0'



cap2 = cv2.VideoCapture(device_name1)
cap1 = cv2.VideoCapture(device_name2)
cap3 = cv2.VideoCapture(device_name3)
cap2.set(3,resolution[0])
cap2.set(4,resolution[1])
cap1.set(3,resolution[0])
cap1.set(4,resolution[1])
cap3.set(3,resolution[0])
cap3.set(4,resolution[1])
i=0
while(True):
    starttime=time.time()
    # Capture frame-by-frame
    bool_retrieve1 = cap1.grab()
    bool_retrieve2 = cap2.grab()
    bool_retrieve3 = cap3.grab()
    ret, frame1 = cap1.retrieve()
    ret, frame2 = cap2.retrieve()
    ret, frame3 = cap3.retrieve()
    i=i+1
    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    #cv2.imwrite('/media/nvidia/Files/1_'+str(i)+'.png',depth_image)
    #cv2.imwrite('/media/nvidia/Files/2_'+str(i)+'.png',frame2)
    images=np.hstack((frame1, frame3,frame2))
    #cv2.imwrite('/media/nvidia/Files/1_'+str(i)+'.png',images)
    cv2.imshow('frame3',images)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    print((time.time() - starttime))
    #time.sleep(1/record_FPS-((time.time() - starttime) % (1/record_FPS)))

# When everything done, release the capture
cap1.release()
cv2.destroyAllWindows()
