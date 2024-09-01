#!/usr/bin/env python3

# This script detects ArUco markers in the camera feed.
import cv2

# initialize camera
cap = cv2.VideoCapture(0)

# setup aruco dictionary and parameters for detection
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
parameters = cv2.aruco.DetectorParameters()
parameters.cornerRefinementMethod = cv2.aruco.CORNER_REFINE_CONTOUR
detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

while True:
    # capture frame
    ret, frame = cap.read()

    # convert to grey scale for detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # look for markers
    try:
        corners, ids, rejectedImgPoints = detector.detectMarkers(gray)
    except Exception as e:
        print(e)
        continue
    if corners:  # if markers are found mark them in the frame
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)

    # show it on screen
    cv2.imshow("camera", frame)
    # press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# cleanup
cap.release()
cv2.destroyAllWindows()
