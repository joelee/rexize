"""
Rexize Extension to downscale an image to RGB format.
"""
import cv2
import numpy as np
from PIL import Image

from base_extension import BaseExtension


class RexizeExtension(BaseExtension):
    def __init__(self):
        self._exposure = 0
        self._image = None

    def apply(self, image: Image.Image):
        self._image = image
        self._exposure = self._calculate_exposure()
        return self._normalize_exposure()

    def _calculate_average_brightness(self):
        image = cv2.cvtColor(np.array(self._image), cv2.COLOR_RGB2BGR)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        return np.mean(hsv[:, :, 2])

    def about(self) -> str:
        return "Detects and normalizes the exposure to ensure uniform exposure across all images"
