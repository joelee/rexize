"""
BaseExtension class is an abstract class that defines the structure of the
extension classes.
"""

from abc import ABC, abstractmethod

from image import RexizeImage


class BaseExtension(ABC):
    @abstractmethod
    def apply(self, image: RexizeImage):
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

    def finalise(self, image: RexizeImage):  # noqa: B027
        """
        Finalise the extension (Optional Method).
        Overwrite this to implement finalisation.
        :param image:
        :return:
        """
        pass

    def has_finaliser(self):
        """
        Check if the extension has a finaliser method.
        :return:
        """
        return hasattr(self, "finalise")
