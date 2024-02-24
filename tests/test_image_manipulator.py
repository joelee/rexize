import os
import shutil
import tempfile
from uuid import uuid4

import pytest
from icecream import ic
from image_manipulator import ImageFormat, ImageManipulator, ImageSizeUnit

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


def test_image_manipulator_resize():
    # Arrange
    image = ImageManipulator(SOURCE_IMAGE)
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


def test_image_manipulator_save():
    # Arrange
    image = ImageManipulator(SOURCE_IMAGE)
    dest_path = os.path.join(OUTPUT_BASE_FOLDER, f"{uuid4()}.png")

    # Act
    image.resize(100, 100)
    image.save(dest_path)

    # Assert
    assert image.width == 100
    assert os.path.exists(dest_path)


def test_image_manipulator_save_with_format():
    # Arrange
    image = ImageManipulator(SOURCE_IMAGE)
    dest_path = os.path.join(OUTPUT_BASE_FOLDER, f"{uuid4()}.jpg")

    # Act
    ic(dest_path)
    ic(ImageFormat.JPEG.value)
    image.downscale_to_rgb().rotate(90).downscale_to_grayscale()
    image.save(dest_path, format=ImageFormat.JPEG, quality=75)

    # Assert
    assert os.path.exists(dest_path)


def test_image_manipulator_invalid_source_image():
    # Arrange
    invalid_image_path = "tests/data/invalid_img.png"

    # Act & Assert
    with pytest.raises(FileNotFoundError):
        ImageManipulator(invalid_image_path)


def test_image_manipulator_invalid_resize():
    # Arrange
    image = ImageManipulator(SOURCE_IMAGE)

    # Act & Assert
    with pytest.raises(ValueError):
        image.resize(100, [120, 120])
    with pytest.raises(ValueError):
        image.resize("invalid", 100)
