#!/usr/bin/env python3

import cv2
from aruco_svg import generate_svg_path
from utils import create_svg_path_from_loops, make_square

if __name__ == "__main__":
    aruco_type = cv2.aruco.DICT_4X4_50
    marker_size = (
        cv2.aruco.getPredefinedDictionary(aruco_type).markerSize + 2
    )  # add 2 for black border
    checker_size = marker_size / 0.75  # make the marker 75% of the checkerboard square
    checker_width = 13
    checker_height = 7
    checker_size_mm = 36
    mm_per_pixel = checker_size_mm / checker_size
    checker_width_mm = checker_width * checker_size * checker_size_mm
    checker_height_mm = checker_height * checker_size * checker_size_mm
    svg_width = checker_width * checker_size + 2
    svg_height = checker_height * checker_size + 2
    svg_width_mm = svg_width * mm_per_pixel
    svg_height_mm = svg_height * mm_per_pixel

    marker_id = 0
    paths = []
    for row in range(checker_height):
        for col in range(checker_width):
            if row % 2 == col % 2:
                square_loop = make_square(
                    (col * checker_size, row * checker_size), checker_size
                )
                square_path = create_svg_path_from_loops([square_loop])
                paths.append(square_path)
            else:
                path = generate_svg_path(marker_id, aruco_type)
                x = col * checker_size + 1
                y = row * checker_size + 1
                paths.append(f'<g transform="translate({x}, {y})">{path}</g>')
                marker_id += 1
    header = (
        f'<svg xmlns="http://www.w3.org/2000/svg"\n'
        + f'  viewBox="0 0 {svg_width} {svg_height}"\n'
        + f'  width="{svg_width_mm}mm" height="{svg_height_mm}mm"\n'
        + f'  style="background: white">\n'
        + f'<g transform="translate(1, 1)">'
    )
    footer = "</g>\n</svg>"
    svg = "\n".join([header] + paths + [footer])
    with open("charuco.svg", "w") as f:
        f.write(svg)
