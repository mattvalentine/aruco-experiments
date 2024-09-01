#!/usr/bin/env python3

# This script generates a set of 50 ArUco markers in SVG format.

import cv2
from aruco_svg import generate_svg_file


if __name__ == "__main__":
    aruco_type = cv2.aruco.DICT_4X4_50
    marker_size_mm = 50  # note that this does not include white border
    for marker_id in range(50):
        generate_svg_file(marker_id, aruco_type, marker_size_mm)
