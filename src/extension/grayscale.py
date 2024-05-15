"""
Rexize Extension to downscale an image to Gray Scale format.
"""
from PIL import Image

from base_extension import BaseExtension


class RexizeExtension(BaseExtension):
    def apply(self, image: Image.Image):
        return image.convert("L")

    def about(self) -> str:
        return "Convert image to grayscale format"
