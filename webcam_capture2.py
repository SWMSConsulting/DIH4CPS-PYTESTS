# import numpy as np
from cv2 import cv2
import datetime

cap = cv2.VideoCapture('rtsp://admin:admin@192.168.8.108:8554')

if not cap.isOpened():
    print("Can not open camera")
    exit()

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# initialize video writer
fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
fps = 30
video_filename = 'output.avi'
out = cv2.VideoWriter(video_filename, fourcc, fps, (frame_width, frame_height))

videolength = 5

start = datetime.datetime.now()

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        frame = cv2.flip(frame,0)

        # write the flipped frame
        out.write(frame)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('frame',gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        now = datetime.datetime.now()
        l: datetime.timedelta = now - start
        if l.seconds > videolength:
            break
    else:
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()