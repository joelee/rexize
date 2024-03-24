import os
from typing import Self

from PIL import Image

from cli import CLI
from image import ImageFormat, ImageSizeUnit


class ImageManipulator:
    def __init__(self, img_path: str, cli: CLI | None = None):
        self._cli = cli if cli else CLI()
        self._src_img = img_path
        self._image = None
        self._size = None
        if not os.path.exists(img_path):
            raise FileNotFoundError(f"File not found at {img_path}")

    @property
    def image(self) -> Image.Image:
        if not self._image:
            self._image = Image.open(self._src_img)
            self._size = self._image.size
            self._cli.verbose(
                f"Opened image: {self._src_img} ({self._size[0]}x{self._size[1]})"
            )
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
        self,
        width: ImageSizeUnit | int | str,
        height: ImageSizeUnit | int | str,
        max_size: ImageSizeUnit | int = 0,
    ) -> Self:
        o_width = self.width
        o_height = self.height
        self._image = self.image.resize(self._get_new_size(width, height, max_size))
        self._cli.verbose(
            f"Resized image from {o_width}x{o_height} to {self.width}x{self.height}"
        )
        return self

    def convert(self, mode: str) -> Self:
        self._image = self.image.convert(mode)
        self._cli.verbose(f"Converted image to: {mode}")
        return self

    def downscale_to_rgb(self) -> Self:
        return self.convert("RGB")

    def downscale_to_grayscale(self) -> Self:
        return self.convert("L")

    def rotate(self, angle: int) -> Self:
        self._image = self.image.rotate(angle)
        self._cli.verbose(f"Rotated image by: {angle} degrees")
        return self

    def save(
        self,
        dest_path: str | None = None,
        format: ImageFormat = ImageFormat.Default,
        **kwargs,
    ) -> Self:
        self._cli.verbose(f"Saving image to: {dest_path}")
        self.image.save(dest_path, format=format.value, **kwargs)
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
    def _convert_unit_to_int(
        value: ImageSizeUnit | int | str, source: int | None
    ) -> int:
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
