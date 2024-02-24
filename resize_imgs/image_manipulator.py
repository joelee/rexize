import os
import re
from enum import Enum
from typing import Self

from icecream import ic
from PIL import Image


class ImageFormat(Enum):
    Default = None
    JPEG = "JPEG"
    PNG = "PNG"
    BMP = "BMP"
    GIF = "GIF"
    TIFF = "TIFF"
    WEBP = "WEBP"


class ImageSizeUnit:
    def __init__(self, value: str | int):
        chk = re.match(r"^(\d+)(%|px)?$", str(value))
        if not chk:
            raise ValueError(
                f"Invalid value for ImageSizeUnit ({value}): "
                "should be a valid integer with optional % suffix"
            )
        self._value = int(chk.group(1))
        self._unit = "px" if not chk.group(2) else str(chk.group(2))

    @property
    def value(self) -> int:
        return self._value

    @property
    def is_percentage(self) -> bool:
        return self.unit == "%"

    @property
    def unit(self) -> str:
        return self._unit

    def calc_value(self, source_px: int) -> int:
        if self.is_percentage:
            return int((self.value / 100) * source_px)
        return self.value


class ImageManipulator:
    def __init__(self, img_path: str):
        self._src_img = img_path
        self._image = None

        if not os.path.exists(img_path):
            raise FileNotFoundError(f"File not found at {img_path}")

    @property
    def image(self) -> Image.Image:
        if not self._image:
            self._image = Image.open(self._src_img)
        return self._image

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
        self, width: ImageSizeUnit | int | str, height: ImageSizeUnit | int | str
    ) -> Self:
        new_size = (
            self._convert_unit_to_int(width, self.width),
            self._convert_unit_to_int(height, self.height),
        )
        self._image = self.image.resize(new_size)
        return self

    def convert(self, mode: str) -> Self:
        self._image = self.image.convert(mode)
        return self

    def downscale_to_rgb(self) -> Self:
        return self.convert("RGB")

    def downscale_to_grayscale(self) -> Self:
        return self.convert("L")

    def rotate(self, angle: int) -> Self:
        self._image = self.image.rotate(angle)
        return self

    def save(
        self,
        dest_path: str | None = None,
        format: ImageFormat = ImageFormat.Default,
        **kwargs,
    ) -> Self:
        ic(dest_path)
        ic(format)

        self.image.save(dest_path, format=format.value, **kwargs)
        return self

    @staticmethod
    def _convert_unit_to_int(value: ImageSizeUnit | int | str, source: int) -> int:
        if isinstance(value, int):
            return value

        if isinstance(value, str):
            value = ImageSizeUnit(value)

        if isinstance(value, ImageSizeUnit):
            return value.calc_value(source)

        raise ValueError(f"Invalid value for ImageSizeUnit: ({value})")
