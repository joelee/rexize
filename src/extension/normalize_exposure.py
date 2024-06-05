"""
Rexize Extension to downscale an image to RGB format.
"""

import cv2
import numpy as np
from base_extension import BaseExtension
from PIL import Image


class RexizeExtension(BaseExtension):
    def __init__(self):
        self._total_exposure = 0
        self._total_images = 0
        super().__init__()

    @property
    def average_exposure(self):
        return self._total_exposure / self._total_images

    def apply(self, image: Image.Image):
        self._total_exposure += self._calculate_exposure(image)
        self._total_images += 1
        return

    def finalise(self, image: Image.Image):
        pass

    def _calculate_average_brightness(self):
        image = cv2.cvtColor(np.array(self._image), cv2.COLOR_RGB2BGR)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        return np.mean(hsv[:, :, 2])

    def about(self) -> str:
        return (
            "Detects and normalizes the exposure to ensure uniform exposure "
            "across all images"
        )
