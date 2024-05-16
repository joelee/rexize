import re
from enum import Enum


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

    def calc_value(self, source_px: int | None) -> int:
        if self.is_percentage and source_px is not None:
            return int((self.value / 100) * source_px)
        return self.value

    def __str__(self) -> str:
        return f"{self.value}{self.unit}"

    def __repr__(self) -> str:
        return f"ImageSizeUnit({self.value}{self.unit})"
