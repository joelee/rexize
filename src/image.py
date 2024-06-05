import os
from typing import Any, Self

import cv2
import numpy as np
from console import console
from image_util import ImageFormat, ImageSizeUnit
from PIL import Image


class RexizeImage:
    def __init__(self, src_file: str, target_file: str):
        self._src_img = src_file
        self._target_img = target_file
        self._image = None
        if not os.path.exists(src_file):
            raise FileNotFoundError(f"File not found at {src_file}")

    def load_target_if_exists(self):
        try:
            self._image = Image.open(self._target_img)
            console.verbose(
                f"Target image loaded: {self._target_img} ({self.width}x{self.height})"
            )
        except FileNotFoundError:
            pass
        return self

    @property
    def image(self) -> Image.Image:
        if not self._image:
            self._image = Image.open(self._src_img)
            console.verbose(
                f"Opened image: {self._src_img} ({self.width}x{self.height})"
            )
        return self._image

    @image.setter
    def image(self, img: Image.Image):
        self._image = img

    @property
    def image_cv2(self):
        return cv2.cvtColor(np.array(self._image.convert("RGB")), cv2.COLOR_RGB2BGR)

    @image_cv2.setter
    def image_cv2(self, image_cv2: np.ndarray):
        self._image = Image.fromarray(cv2.cvtColor(image_cv2, cv2.COLOR_BGR2RGB))

    @property
    def size(self) -> tuple[int, int]:
        return self.image.size

    @property
    def width(self) -> int:
        return self.size[0]

    @property
    def height(self) -> int:
        return self.size[1]

    def resize(
        self,
        width: ImageSizeUnit | int | str,
        height: ImageSizeUnit | int | str,
        max_size: ImageSizeUnit | int = 0,
    ) -> Self:
        o_width = self.width
        o_height = self.height
        self._image = self.image.resize(self._get_new_size(width, height, max_size))
        console.verbose(
            f"Resized image from {o_width}x{o_height} to {self.width}x{self.height}"
        )
        return self

    def convert(self, mode: str) -> Self:
        self._image = self.image.convert(mode)
        console.verbose(f"Converted image to: {mode}")
        return self

    def rotate(self, angle: int) -> Self:
        self._image = self.image.rotate(angle)
        console.verbose(f"Rotated image by: {angle} degrees")
        return self

    def save(
        self,
        img_format: ImageFormat = ImageFormat.Default,
        **kwargs,
    ) -> Self:
        console.verbose(f"Saving image to: {self._target_img}")
        self.image.save(self._target_img, format=img_format.value, **kwargs)
        return self

    def _get_new_size(
        self,
        width: ImageSizeUnit | int | str,
        height: ImageSizeUnit | int | str,
        max_size: ImageSizeUnit | int | str,
    ) -> tuple[int, int]:
        new_width = self._convert_unit_to_int(width, self.width)
        new_height = self._convert_unit_to_int(height, self.height)
        max_size = self._convert_unit_to_int(max_size, None)

        if max_size > 0:
            if new_width == 0 and new_height == 0:
                new_width = self.width
                new_height = self.height
            new_width, new_height = self._get_new_size_with_max_size(
                new_width, new_height, max_size
            )

        # Calculate new width and height if any of them is 0 based on aspect ratio
        if new_width == 0:
            new_width = int((new_height / self.height) * self.width)
        if new_height == 0:
            new_height = int((new_width / self.width) * self.height)

        if new_width == 0 and new_height == 0 and max_size == 0:
            raise ValueError("Both width and height cannot be 0 at the same time.")

        return new_width, new_height

    @staticmethod
    def _convert_unit_to_int(value: Any, source: int | None) -> int:
        if isinstance(value, int):
            return value

        if isinstance(value, str):
            value = ImageSizeUnit(value)

        if isinstance(value, ImageSizeUnit):
            return value.calc_value(source)

        raise ValueError(f"Invalid value for ImageSizeUnit: ({value})")

    @staticmethod
    def _get_new_size_with_max_size(
        width: int, height: int, max_size: int
    ) -> tuple[int, int]:
        if width > max_size:
            height = int((max_size / width) * height)
            width = max_size
        if height > max_size:
            width = int((max_size / height) * width)
            height = max_size
        return width, height
