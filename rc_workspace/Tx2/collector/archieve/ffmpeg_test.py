import ffmpeg
stream = ffmpeg.input('/dev/v4l/by-id/usb-046d_HD_Webcam_C615_794F2390-video-index0')

stream = ffmpeg.output(stream, './output6.mp4')
ffmpeg.run(stream)
