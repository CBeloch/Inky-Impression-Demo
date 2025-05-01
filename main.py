
import argparse
import pathlib
import sys

from image import Image, ResizeMode
from PIL.Image import Transpose

import inky

parser = argparse.ArgumentParser()
parser.add_argument("--file", "-f", type=pathlib.Path, help="Image file")

args, _ = parser.parse_known_args()

display = inky.auto()

# Open Image
image = Image.open(args.file)
# Rotate
image = image.transpose(Transpose.ROTATE_90)
# Scale to screen size
image = image.scale(display.resolution, ResizeMode.SCALE_TO_FILL)

display.set_image(image, saturation = 0.5)
display.show()