
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

image = Image.open(args.file)

# def keepAspectResize(input, targetWidth):
#     print("targetWidth: %d - input: %d" % (targetWidth, input.size[0]))
#     wpercent = (targetWidth/float(input.size[0]))
#     print("resizing by %s" % wpercent)
#     hsize = int((float(input.size[1])*float(wpercent)))
#     return input.resize((targetWidth,hsize))

print("Input image size %d x %d" % image.size)
rotatedImage = image.transpose(Transpose.ROTATE_90)
print("rotated image size %d x %d" % rotatedImage.size)

# if resizedimage.size[1] < display.resolution[1]:
#   print("Adding Fill elements")
#   diff = display.resolution[1] - resizedimage.size[1]
#   resizedimage = ImageOps.expand(resizedimage, (0, int(diff/2), 0, int(diff/2)), (255, 255, 255))
# elif resizedimage.size[1] > display.resolution[1]:
#   print("Cropping")
#   diff = resizedimage.size[1] - display.resolution[1]
#   if diff % 2 == 1:
#       resizedimage = ImageOps.crop(resizedimage, (0, int(diff/2), 0, int(diff/2) + 1))
#   else:
#       resizedimage = ImageOps.crop(resizedimage, (0, int(diff/2), 0, int(diff/2)))

# display.set_image(resizedimage, saturation = 0.9)

scaledImage = rotatedImage.scale(display.resolution, ResizeMode.SCALE_TO_FIT)
print("scaled image size %d x %d" % scaledImage.size)

display.set_image(scaledImage, saturation = 0.5)
display.show()