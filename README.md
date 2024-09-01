# Aruco SVG Generation

There are a few SVG generators for Aruco markers, but the vectors they produce tend to include extraneous paths that are not suited for laser cutting, vinyl cutting, or other path based fabrication or printing methods.

This repo has some tools for making Aruco markers using OpenCV, PyClipper, and raw strings for the SVG itself. The resulting SVGs are very light weight, and import well into CAD/CAM tools.

Here's an example of a 4x4 Marker with ID 0:

```svg
<svg xmlns="http://www.w3.org/2000/svg"
  viewBox="-0.5 -0.5 7 7"
  width="58.333333333333336mm" height="58.333333333333336mm"
  style="background: white">
<path fill="black" stroke="none" d="M 6 6 L 0 6 L 0 0 L 6 0 Z M 3 1 L 3 2 L 4 2 L 4 3 L 3 3 L 3 5 L 4 5 L 4 4 L 5 4 L 5 1 Z M 2 2 L 2 3 L 3 3 L 3 2 Z M 1 1 L 1 2 L 2 2 L 2 1 Z" />
</svg>
```

## Usage

Install prereqs with `pip install -r requirements.txt`. (Note this installs OpenCV, so you may want a venv or conda environment to manage versions between projects)

The valuable part of this repo is in aruco_svg.py, which has 3 functions:

### generate_svg_path

```python
import cv2
from aruco_svg import generate_svg_path

# To generate an SVG path (without physical units) for a given ArUco marker:
marker_id = 0
marker_type = cv2.aruco.DICT_4X4_50
svg_path_only = generate_svg_path(marker_id, marker_type)
print(f"Path: {svg_path_only}")
```

### generate_svg_string

```python
import cv2
from aruco_svg import generate_svg_string

# To generate a full SVG (with header) as a string for a given ArUco marker with pyhsical units:
marker_id = 1
marker_type = cv2.aruco.DICT_5X5_50
marker_size_mm = 50
full_svg_string = generate_svg_string(marker_id, marker_type, marker_size_mm)
print(f"Full SVG: {full_svg_string}")
```

### generate_svg_file

```python
import cv2
from aruco_svg import generate_svg_file

# To generate a full SVG file for a given ArUco marker and save it:
marker_id = 2
marker_type = cv2.aruco.DICT_7X7_50
marker_size_mm = 75
filename = "marker.svg"
generate_svg_file(marker_id, marker_type, marker_size_mm, filename)
```

## Demos

There are a few demos included as well:

### make_markers.py

This generates 50 SVG files of 4x4 aruco markers.

### make_charuco.py

This generates a 13x7 charuco board as an svg combining generated aruco paths with other geometry.

### detect_markers.py

Not really a demo, but useful to do quick tests with a webcam.

## Notes

The SVG is generated with a white margin, but does not generate a path for that border.

If you're going to modify this file, or do other work with pyclipper, I recommend installing and running pybind11-stubgen to enable IDE integrations.

```bash
pip install pybind11-stubgen
pybind11-stubgen pyclipper -o typings
```

OpenCV has been messing with the Aruco library structure, so having a newer OpenCV version for this can be helpful, so if you get an error try version 4.10 of OpenCV.
