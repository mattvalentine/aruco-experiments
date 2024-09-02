#!/usr/bin/env python3
import cv2

# Create a Charuco board that matches the SVG we created
dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
board = cv2.aruco.CharucoBoard((13, 7), 0.036, 0.027, dictionary=dictionary)

# Save the board to a file to compare with our SVG board
cv2.imwrite("charuco.png", board.generateImage((1920, 1080)))

# Create a detector for the board
params = cv2.aruco.CharucoParameters()
detector = cv2.aruco.CharucoDetector(board, params)

# initialize camera
cap = cv2.VideoCapture(0)

while True:
    # capture frame
    ret, frame = cap.read()

    # convert to grey scale for detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # look for markers and board
    try:
        charuco_corners, ids, marker_corners, marker_ids = detector.detectBoard(gray)
    except Exception as e:
        print(e)
        continue
    if charuco_corners is not None:  # if board is found mark corners in the frame
        cv2.aruco.drawDetectedCornersCharuco(frame, charuco_corners, ids)
    if marker_corners is not None:  # if markers are found mark them in the frame
        cv2.aruco.drawDetectedMarkers(frame, marker_corners, marker_ids)
    # show it on screen
    cv2.imshow("camera", frame)
    # press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
