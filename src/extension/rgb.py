"""
Rexize Extension to downscale an image to RGB format.
"""
from PIL import Image

from base_extension import BaseExtension


class RexizeExtension(BaseExtension):
    def apply(self, image: Image.Image):
        return image.convert("RGB")

    def about(self) -> str:
        return "Convert image to RGB format"
