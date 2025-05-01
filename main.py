
import argparse
import pathlib
import sys

from image import Image, ResizeMode
from PIL.Image import Transpose

import inky

parser = argparse.ArgumentParser()
parser.add_argument("--file", "-f", type=pathlib.Path, help="Image file")
parser.add_argument("--rotation", "-r", type=int, help="Screen rotation", default=0)
parser.add_argument("--scale", "-s", type=str, help="Scale Mode - fill or fit", default="fit")

args, _ = parser.parse_known_args()

display = inky.auto()

# Open Image
image = Image.open(args.file)
# Rotate
transposing = None
match args.rotation:
    case 90:
        transposing = Transpose.ROTATE_90
    case 180:
        transposing = Transpose.ROTATE_180
    case -90:
        transposing = Transpose.ROTATE_270
    case 270:
        transposing = Transpose.ROTATE_270

if transposing:
    image = image.transpose(transposing) 

# Scale to screen size
resizeMode = ResizeMode.SCALE_TO_FIT
match args.scale:
    case "fit":
        resizeMode = ResizeMode.SCALE_TO_FIT
    case "fill":
        resizeMode = ResizeMode.SCALE_TO_FILL

image = image.scale(display.resolution, resizeMode)

display.set_image(image, saturation = 0.5)
display.show()