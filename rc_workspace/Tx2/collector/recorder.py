import pyrealsense2 as rs
import numpy as np
import time
import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()

config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)


record_FPS=10
# Start streaming
pipeline.start(config)

try:
    starttime=time.time()
    while True:

        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()

        color_frame = frames.get_color_frame()


        # Convert images to numpy arrays

        color_image = np.asanyarray(color_frame.get_data())


        # Stack both images horizontally
        images =color_image
        #print('hehe')
        # Show images
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', images)
        cv2.waitKey(1)
        time.sleep(1/record_FPS-((time.time() - starttime) % (1/record_FPS)))
finally:

    # Stop streaming
    pipeline.stop()
