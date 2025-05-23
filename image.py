from enum import Enum
from typing import IO, Any, Literal, Protocol

from PIL import Image as PILImage, ImageOps
from PIL.Image import Transpose

from operator import sub
import math

class ResizeMode(Enum):
    SCALE_TO_FIT = 1
    SCALE_TO_FILL = 2

class Image(object):
    def __init__(self,img):
        self._img=img
    def __getattr__(self,key):
        if key == '_img':
            #  http://nedbatchelder.com/blog/201010/surprising_getattr_recursion.html
            raise AttributeError()
        return getattr(self._img,key)
    
    @staticmethod
    def open(
        fp: str,
        mode: Literal["r"] = "r",
        formats: list[str] | tuple[str, ...] | None = None,
    ):
        return Image(PILImage.open(fp, mode, formats))
    
    def transpose(self, method: Transpose):
        return Image(self._img.transpose(method))

    def scale(self, targetDimension: tuple[int], resizeMode: ResizeMode = ResizeMode.SCALE_TO_FILL, match: bool = True):
        image = self

        match resizeMode:
            case ResizeMode.SCALE_TO_FILL:
                image = Image(ImageOps.fit(image._img, targetDimension))
            case ResizeMode.SCALE_TO_FIT:
                image = Image(ImageOps.pad(image._img, targetDimension, color="#fff"))
        
        return image
    
    def match(self, targetDimension: tuple[int]):
        diffs = tuple(map(sub, self.size, targetDimension))
        left, right, top, bottom = (diffs[0] // 2, diffs[0] // 2, diffs[1] // 2, diffs[1] // 2)

        if diffs[0] % 2 != 0:
            adjustment = 1 #if diffs[0] > 0 else -1
            right = right + adjustment
        
        if diffs[1] % 2 != 0:
            adjustment = 1 #if diffs[1] > 0 else -1
            bottom = bottom + adjustment

        # print("diffs", diffs)
        # print("crops:", (left, right, top, bottom))

        output = self

        # fix horizontal size
        if diffs[0] < 0:
            # expand width
            output = ImageOps.expand(output, (abs(left), 0, abs(right), 0), (255, 255, 255))
        else:
            # crop width
            output = ImageOps.crop(output, (left, 0, right, 0))

        # fix vertical size
        if diffs[1] < 0:
            # expand height
            output = ImageOps.expand(output, (0, abs(top), 0, abs(bottom)), (255, 255, 255))
        else:
            # crop height
            output = ImageOps.crop(output, (0, top, 0, bottom))

        return Image(output)

