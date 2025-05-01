
import argparse
import pathlib
import sys

from image import Image, ResizeMode
from PIL.Image import Transpose

import gpiod
import gpiodevice
from gpiod.line import Bias, Direction, Edge

import inky

# Parse Arguments
parser = argparse.ArgumentParser()
parser.add_argument("--file", "-f", type=pathlib.Path, help="Image file")
parser.add_argument("--rotation", "-r", type=int, help="Screen rotation", default=0)
parser.add_argument("--scale", "-s", type=str, help="Scale Mode - fill or fit", default="fit")

args, _ = parser.parse_known_args()

# Setup Buttons
SW_A = 5
SW_B = 6
SW_C = 16  # Set this value to '25' if you're using a Impression 13.3"
SW_D = 24

BUTTONS = [SW_A, SW_B, SW_C, SW_D]
# These correspond to buttons A, B, C and D respectively
LABELS = ["A", "B", "C", "D"]

INPUT = gpiod.LineSettings(direction=Direction.INPUT, bias=Bias.PULL_UP, edge_detection=Edge.FALLING)
chip = gpiodevice.find_chip_by_platform()
OFFSETS = [chip.line_offset_from_id(id) for id in BUTTONS]
line_config = dict.fromkeys(OFFSETS, INPUT)
request = chip.request_lines(consumer="spectra6-buttons", config=line_config)


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
#display.show()

def handle_button(event):
    index = OFFSETS.index(event.line_offset)
    gpio_number = BUTTONS[index]
    label = LABELS[index]
    print(f"Button press detected on GPIO #{gpio_number} label: {label}")

while True:
    for event in request.read_edge_events():
        handle_button(event)