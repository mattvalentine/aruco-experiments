import cv2
import numpy as np
import pyclipper


def make_square(point, width=1):
    # Make a simple square from upper left corner
    return [
        point,
        (point[0] + width, point[1]),
        (point[0] + width, point[1] + width),
        (point[0], point[1] + width),
    ]


def get_loops(marker_size, cut_squares):
    # Pyclipper can do geometric operations on loops of points
    clipper = pyclipper.Pyclipper()
    # Make a square loop for the perimeter of the marker
    clipper.AddPaths([make_square((0, 0), marker_size)], pyclipper.PT_SUBJECT)
    # Setup square to cut out
    clipper.AddPaths([make_square(square) for square in cut_squares], pyclipper.PT_CLIP)
    # cut out the squares and return
    return clipper.Execute(pyclipper.CT_DIFFERENCE)


def create_svg_paths(marker_size, svg_mm, cut_squares):
    loops = get_loops(marker_size, cut_squares)
    path_string_list = []
    for loop in loops:
        if len(loop) < 1:
            # skip empty loops
            continue
        point = loop.pop(0)  # get the first point
        # Move to fist point
        path_string_list.append(f"M {point[0]} {point[1]}")
        while loop:
            point = loop.pop(0)  # get the next point
            # draw a line to the next point
            path_string_list.append(f"L {point[0]} {point[1]}")
        # connect back to first point to close the loop
        path_string_list.append(f"Z")

    # wrap the whole thing in an svg header and one big path element
    svg_size = marker_size + 1
    # marker_size + 2 accounts for border around outer edge
    return f"""<svg xmlns="http://www.w3.org/2000/svg" 
  viewBox="-0.5 -0.5 {svg_size} {svg_size}"
  width="{svg_mm}mm" height="{svg_mm}mm"
   style="background: white">
  <path fill="none" stroke="none" stroke-width="0.01" d="M -0.5 -0.5 h {svg_size} v {svg_size} h -{svg_size} Z"/>
  <path fill-rule="evenodd" fill="black" stroke="none" d="{" ".join(path_string_list)}" />
</svg>"""


def generate_svg_marker(marker_id, marker_size_mm, aruco_type):
    aruco_dict = cv2.aruco.getPredefinedDictionary(aruco_type)
    marker_size = (
        aruco_dict.markerSize + 2
    )  # minsize = size + 1 on each side for border
    svg_size = marker_size + 1  # padded for white space
    svg_scale = marker_size_mm / marker_size
    svg_mm = svg_size * svg_scale

    marker = cv2.aruco.generateImageMarker(aruco_dict, marker_id, marker_size)
    ys, xs = np.where(marker == 255)
    return create_svg_paths(marker_size, svg_mm, list(zip(xs, ys)))


if __name__ == "__main__":
    aruco_type_dict = {
        getattr(cv2.aruco, aruco_type): aruco_type
        for aruco_type in filter(lambda x: x.startswith("DICT"), dir(cv2.aruco))
    }
    aruco_type = cv2.aruco.DICT_4X4_50
    marker_size_mm = 50  # note that this does not include white border

    for marker_id in range(50):
        svg_string = generate_svg_marker(marker_id, marker_size_mm, aruco_type)
        with open(
            f"Aruco-{aruco_type_dict[aruco_type]}-Marker-{marker_id}-{marker_size_mm}mm.svg",
            "w",
        ) as svg_file:
            svg_file.write(svg_string)
