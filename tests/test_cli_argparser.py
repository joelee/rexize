import os
import shutil
import tempfile
from uuid import uuid4

import pytest

from cli import CLI

# Constants
SOURCE_FOLDER = "tests/data/test_dir_tree"
OUTPUT_BASE_FOLDER = os.path.join(tempfile.gettempdir(), "resize_imgs_argparser_test")


def setup_module(module):
    # Create Output Base Folder if not exists
    if not os.path.exists(OUTPUT_BASE_FOLDER):
        os.makedirs(OUTPUT_BASE_FOLDER)


def teardown_module(module):
    # Delete Output Base Folder if exists
    if os.path.exists(OUTPUT_BASE_FOLDER):
        shutil.rmtree(OUTPUT_BASE_FOLDER)


@pytest.fixture(autouse=True)
def output_folder():
    # Setup
    output_folder = os.path.join(OUTPUT_BASE_FOLDER, str(uuid4()))

    yield output_folder

    # Teardown
    # Delete Output Folder if exists for fresh testing
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)


def test_argparser_in_pixels(output_folder):
    input = [
        "-i",
        SOURCE_FOLDER,
        "-o",
        output_folder,
        "-W",
        "100",
        "-H",
        "200px",
        "-f",
        "JPEG",
    ]

    cli = CLI(input)
    assert cli.args.input_folder == SOURCE_FOLDER
    assert cli.args.output_folder == output_folder
    assert cli.args.width.value == 100
    assert cli.args.width.calc_value(12345) == 100
    assert not cli.args.width.is_percentage
    assert cli.args.height.value == 200
    assert cli.args.height.calc_value(54321) == 200
    assert not cli.args.height.is_percentage
    assert cli.args.format.value == "JPEG"


def test_argparser_in_percent(output_folder):
    input = [
        "-i",
        SOURCE_FOLDER,
        "-o",
        output_folder,
        "-W",
        "50%",
        "-H",
        "150%",
        "-f",
        "WEBP",
    ]

    cli = CLI(input)
    assert cli.args.input_folder == SOURCE_FOLDER
    assert cli.args.output_folder == output_folder
    assert cli.args.width.value == 50
    assert cli.args.width.calc_value(500) == 250  # 50% of 500 == 250
    assert cli.args.width.is_percentage
    assert cli.args.height.value == 150
    assert cli.args.height.calc_value(100) == 150  # 150% of 100 == 150
    assert cli.args.height.is_percentage
    assert cli.args.format.value == "WEBP"


def test_argparser_invalid_folder():
    input = [
        "-i",
        "INVALID",
        "-o",
        OUTPUT_BASE_FOLDER,
        "-W",
        "100",
        "-H",
        "200px",
        "-f",
        "JPEG",
    ]

    with pytest.raises(FileNotFoundError) as e:
        CLI(input)
    assert str(e.value) == "Input folder not found or readable at INVALID"


def test_argparser_invalid_format(output_folder):
    input = [
        "-i",
        SOURCE_FOLDER,
        "-o",
        output_folder,
        "-W",
        "100",
        "-H",
        "200px",
        "-f",
        "INVALID",
    ]

    with pytest.raises(ValueError) as e:
        CLI(input)
    assert str(e.value) == "Invalid image format"


def test_argparser_readonly_output_folder():
    readonly_folder = "/usr/bin"  # A system folder that is readonly.
    # Only works on Unix-like & Mac OS systems

    input = [
        "-i",
        SOURCE_FOLDER,
        "-o",
        readonly_folder,
        "-W",
        "100",
        "-H",
        "200px",
        "-f",
        "JPEG",
    ]

    with pytest.raises(PermissionError) as e:
        CLI(input)
    assert str(e.value) == f"Output folder not writable at {readonly_folder}"


def test_argparser_pre_processor():
    input = [
        "-i",
        SOURCE_FOLDER,
        "-o",
        "/tmp",
        "-p",
        "FILTER1",
        "-H",
        "200px",
        "-p",
        "Filter2",
        "-f",
        "JPEG",
    ]
    print(input)

    with pytest.raises(ValueError) as e:
        cli = CLI(input)
        print(cli.args)
        assert False
    assert str(e.value) == "Invalid width value"
