"""
BaseExtension class is an abstract class that defines the structure of the extension classes.
"""

from abc import ABC, abstractmethod

from PIL import Image


class BaseExtension(ABC):
    @abstractmethod
    def apply(self, image: Image.Image):
        """
        Apply the extension to the image.
        :param image:
        :return:
        """
        pass

    @abstractmethod
    def about(self) -> str:
        """
        Return information about the extension.
        :return:
        """
        return "Information about the Rexize Extension"

    def has_finaliser(self):
        """
        Check if the extension has a finaliser method.
        :return:
        """
        return hasattr(self, "finalise")
