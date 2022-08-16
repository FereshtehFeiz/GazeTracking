"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""

import cv2
from gaze_tracking import GazeTracking
import csv 

gaze = GazeTracking()
# webcam = cv2.VideoCapture(0)
video = cv2.VideoCapture("video.mp4")
# create the csv file
f = open('out.csv', 'w', newline='')
# add coloumns
fieldnames = ['blink', 'looking']
# create the csv writer and add the headers
writer = csv.writer(f)
writer = csv.DictWriter(f, fieldnames=fieldnames)
writer.writeheader()

while True:
    # We get a new frame from the webcam
    # _, frame = webcam.read()
    _, frame = video.read()

    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)

    frame = gaze.annotated_frame()
    text = ""
    blink = 0

    if gaze.is_blinking():
        text = "Blinking"
        blink = 1
    elif gaze.is_right():
        text = "Looking right"
    elif gaze.is_left():
        text = "Looking left"
    elif gaze.is_center():
        text = "Looking center"
    
    rows = [
        {'blink': blink,
        'looking': text}]
            
     # append the data in the csv
    with open('out.csv', 'w', encoding='UTF8', newline='') as f:
        writer.writerows(rows)

    cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()
    cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

    cv2.imshow("Demo", frame)

    if cv2.waitKey(1) == 27:
        break
   
# webcam.release()
f.close()
cv2.destroyAllWindows()
