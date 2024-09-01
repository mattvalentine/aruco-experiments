import pyclipper


def make_square(point: tuple, width=1):
    # Make a simple square from upper left corner
    return [
        point,
        (point[0] + width, point[1]),
        (point[0] + width, point[1] + width),
        (point[0], point[1] + width),
    ]


def get_loops_from_cut_squares(marker_size, cut_squares):
    # Pyclipper can do geometric operations on loops of points
    clipper = pyclipper.Pyclipper()
    # Make a square loop for the perimeter of the marker
    clipper.AddPaths([make_square((0, 0), marker_size)], pyclipper.PT_SUBJECT)
    # Setup square to cut out
    clipper.AddPaths([make_square(square) for square in cut_squares], pyclipper.PT_CLIP)
    # cut out the squares and return
    return clipper.Execute(pyclipper.CT_DIFFERENCE)


def create_svg_path_from_loops(loops):
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
    # marker_size + 2 accounts for border around outer edge
    return f'<path fill="black" stroke="none" d="{" ".join(path_string_list)}" />'
