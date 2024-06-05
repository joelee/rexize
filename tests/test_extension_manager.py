import pytest
from base_extension import BaseExtension
from extension_manager import ExtensionManager
from PIL import Image

# Constants
SOURCE_IMAGE = "tests/data/test_img.png"  # PNG Image W 440 x H 578
IMAGE = Image.open(SOURCE_IMAGE)


class DummyExtension(BaseExtension):
    def apply(self, image):
        return "applied"

    def finalise(self, image):
        return "finalised"

    def about(self):
        return "Unit Test dummy extension"


def test_built_in_extensions():
    em = ExtensionManager()
    assert em.get("grayscale").about() == "Convert image to grayscale format"
    assert em.get("rgb").about() == "Convert image to RGB format"


def test_register_extension():
    em = ExtensionManager()
    ext = DummyExtension()

    em.register("dummy", ext)
    assert em.get("dummy") == ext

    with pytest.raises(ValueError):
        em.register("dummy", ext)

    with pytest.raises(TypeError):
        em.register("dummy", "ext")


def test_apply_extension():
    em = ExtensionManager()
    ext = DummyExtension()

    em.register("dummy", ext)
    assert em.apply("dummy", IMAGE) == "applied"


def test_finalise_extension():
    em = ExtensionManager()
    ext = DummyExtension()

    em.register("dummy", ext)
    assert em.finalise("dummy", IMAGE) == "finalised"


def test_list_extensions():
    em = ExtensionManager()
    ext = DummyExtension()

    em.register("dummy", ext)
    extensions = em.list_extensions()
    assert "grayscale" in extensions
    assert "rgb" in extensions
