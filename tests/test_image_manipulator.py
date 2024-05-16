import os
import shutil
import tempfile
from uuid import uuid4

import pytest

from image import RexizeImage
from image_util import ImageFormat, ImageSizeUnit

# Constants
SOURCE_IMAGE = "tests/data/test_img.png"  # PNG Image W 440 x H 578
OUTPUT_BASE_FOLDER = os.path.join(tempfile.gettempdir(), "resize_imgs_im_test")


def setup_module(module):
    # Create Output Base Folder if not exists
    if not os.path.exists(OUTPUT_BASE_FOLDER):
        os.makedirs(OUTPUT_BASE_FOLDER)


def teardown_module(module):
    # Delete Output Base Folder if exists
    if os.path.exists(OUTPUT_BASE_FOLDER):
        shutil.rmtree(OUTPUT_BASE_FOLDER)


def test_image_size_unit():
    # Arrange
    size = ImageSizeUnit(100)
    percentage = ImageSizeUnit("50%")

    # Act & Assert
    assert size.value == 100
    assert size.calc_value(200) == 100
    assert not size.is_percentage
    assert percentage.value == 50
    assert percentage.calc_value(200) == 100
    assert percentage.is_percentage
    assert str(size) == "100px"
    assert str(percentage) == "50%"
    assert repr(size) == "ImageSizeUnit(100px)"
    assert repr(percentage) == "ImageSizeUnit(50%)"


def test_image_manipulator_resize():
    # Arrange
    image = RexizeImage(SOURCE_IMAGE)
    original_width = image.width
    width = "25%"
    height = ImageSizeUnit(110)

    # Pre-Assert
    assert image.height != height.value

    # Act
    image.resize(width, height)

    # Assert
    assert image.width == int(original_width * 0.25)
    assert image.height == height.value


def test_image_manipulator_resize_with_aspect_ratio_on_width():
    # Arrange
    image = RexizeImage(SOURCE_IMAGE)
    original_width = image.width
    origial_height = image.height
    width = 0
    height = origial_height * 2

    # Act
    image.resize(width, height)

    # Assert
    assert image.width == int(original_width * 2)
    assert image.height == height


def test_image_manipulator_resize_with_aspect_ratio_on_height():
    # Arrange
    image = RexizeImage(SOURCE_IMAGE)
    original_width = image.width
    origial_height = image.height
    width = "50%"
    height = 0

    # Act
    image.resize(width, height)

    # Assert
    assert image.width == int(original_width * 0.5)
    assert image.height == int(origial_height * 0.5)


def test_image_manipulator_resize_with_zero_width_and_height():
    # Arrange
    image = RexizeImage(SOURCE_IMAGE)

    # Act and Assert
    with pytest.raises(ValueError):
        image.resize(0, 0)


def test_image_manipulator_save():
    # Arrange
    image = RexizeImage(SOURCE_IMAGE)
    dest_path = os.path.join(OUTPUT_BASE_FOLDER, f"{uuid4()}.png")

    # Act
    image.resize(100, 100)
    image.save(dest_path)

    # Assert
    assert image.width == 100
    assert os.path.exists(dest_path)


def test_image_manipulator_save_with_format():
    # Arrange
    image = RexizeImage(SOURCE_IMAGE)
    dest_path = os.path.join(OUTPUT_BASE_FOLDER, f"{uuid4()}.jpg")

    # Act
    image.downscale_to_rgb().rotate(90).downscale_to_grayscale()
    image.save(dest_path, format=ImageFormat.JPEG, quality=75)

    # Assert
    assert os.path.exists(dest_path)


def test_image_manipulator_invalid_source_image():
    # Arrange
    invalid_image_path = "tests/data/invalid_img.png"

    # Act & Assert
    with pytest.raises(FileNotFoundError):
        RexizeImage(invalid_image_path)


def test_image_manipulator_invalid_resize():
    # Arrange
    image = RexizeImage(SOURCE_IMAGE)

    # Act & Assert
    with pytest.raises(ValueError):
        image.resize(100, [120, 120])
    with pytest.raises(ValueError):
        image.resize("invalid", 100)
