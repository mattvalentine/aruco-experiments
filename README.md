# Aruco SVG Generation

There are a few SVG generators for Aruco markers, but the vectors they produce tend to include extraneous paths that are not suited for laser cutting, vinyl cutting, or other path based fabrication or printing methods.

This repo has some tools for making Aruco markers using OpenCV, PyClipper, and raw strings for the SVG itself. The resulting SVGs are very lightweight, and import well into CAD/CAM tools.
