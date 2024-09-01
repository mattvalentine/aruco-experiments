import cv2
import numpy as np
from utils import get_loops_from_cut_squares, create_svg_path_from_loops


def generate_svg_path(marker_id: int, aruco_type: int) -> str:
    """Generate an SVG path for a given ArUco marker.

    Args:
        marker_id (int): Id of the marker to generate
        aruco_type (int): cv2.aruco.DICT_* type of marker to generate

    Returns:
        str: an SVG path string
    """
    aruco_dict = cv2.aruco.getPredefinedDictionary(aruco_type)
    marker_size = aruco_dict.markerSize + 2
    # generate minimum size marker (1px per square)
    marker = cv2.aruco.generateImageMarker(aruco_dict, marker_id, marker_size)
    # find the squares to cut out
    ys, xs = np.where(marker == 255)
    cut_squares = list(zip(xs, ys))
    # get the loops of points to draw
    loops = get_loops_from_cut_squares(marker_size, cut_squares)
    # generate the svg
    path = create_svg_path_from_loops(loops)
    return path


def generate_svg_string(marker_id, aruco_type, marker_size_mm) -> str:
    """Generate an SVG file for a given ArUco marker as a string.

    Args:
        marker_id (_type_): id of the marker to generate
        aruco_type (_type_): cv2.aruco.DICT_* type of marker to generate
        marker_size_mm (_type_): size of the marker in mm (not including white border)

    Returns:
        str: an SVG file as a string
    """
    aruco_dict = cv2.aruco.getPredefinedDictionary(aruco_type)
    marker_size = (
        aruco_dict.markerSize + 2
    )  # minsize = size + 1 on each side for border
    svg_size = marker_size + 1  # padded for white space
    svg_scale = marker_size_mm / marker_size
    svg_mm = svg_size * svg_scale
    header = (
        f'<svg xmlns="http://www.w3.org/2000/svg"\n'
        + f'  viewBox="-0.5 -0.5 {svg_size} {svg_size}"\n'
        + f'  width="{svg_mm}mm" height="{svg_mm}mm"\n'
        + f'  style="background: white">'
    )
    path = generate_svg_path(marker_id, aruco_type)
    footer = "</svg>"
    return "\n".join([header, path, footer])


def generate_svg_file(marker_id, aruco_type, marker_size_mm, filename=None):
    """Generate an SVG file for a given ArUco marker and save it.

    Args:
        marker_id (_type_): id of the marker to generate
        aruco_type (_type_): cv2.aruco.DICT_* type of marker to generate
        marker_size_mm (_type_): size of the marker in mm (not including white border)
        filename (_type_, optional): Name of the svg file to save. Defaults to None.
    """
    aruco_type_dict = {
        getattr(cv2.aruco, aruco_type): aruco_type
        for aruco_type in filter(lambda x: x.startswith("DICT"), dir(cv2.aruco))
    }
    if filename is None:
        filename = f"Aruco-{aruco_type_dict[aruco_type]}-Marker-{marker_id}-{marker_size_mm}mm.svg"
    svg_string = generate_svg_string(marker_id, aruco_type, marker_size_mm)
    with open(filename, "w") as svg_file:
        svg_file.write(svg_string)
    print(f"Saved {filename}")
