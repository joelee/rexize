import argparse
import os

from icecream import ic
from image_manipulator import ImageFormat, ImageSizeUnit


def argparser(cli_args=None):
    parser = argparse.ArgumentParser(
        description="Bulk resize and convert images from a folder recursively."
    )
    parser.add_argument("input_folder", type=str, help="Input folder containing images")
    parser.add_argument(
        "output_folder", type=str, help="Output folder for resized images"
    )
    parser.add_argument(
        "-W",
        "--width",
        type=str,
        default="0",
        help="Width to resize the image. Suffix with for percentage",
    )
    parser.add_argument(
        "-H",
        "--height",
        type=str,
        default="0",
        help="Height to resize the image. Suffix with for percentage",
    )
    parser.add_argument(
        "-f",
        "--format",
        type=str,
        default="WEBP",
        help="Format of the output image: JPEG, PNG, WEBP, GIF, TIFF, BMP",
    )
    parser.add_argument(
        "--rgb", action="store_true", help="Downscale RGBA images to RGB"
    )
    parser.add_argument(
        "--grayscale", action="store_true", help="Downscale images to Grayscale"
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Suppress all output messages, except errors",
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Verbose output for debugging"
    )

    ic(parser)
    ic(cli_args)

    args = parser.parse_args(cli_args)
    ic(args)

    # Validate the input folder exists and readable
    if not os.path.isdir(args.input_folder) or not os.access(
        args.input_folder, os.R_OK
    ):
        raise FileNotFoundError(
            f"Input folder not found or readable at {args.input_folder}"
        )

    # Create the output folder if not exists and check if writable
    if not os.path.exists(args.output_folder):
        os.makedirs(args.output_folder)
    if not os.access(args.output_folder, os.W_OK):
        raise PermissionError(f"Output folder not writable at {args.output_folder}")

    # Validate the width and height
    args.width = ImageSizeUnit(args.width)
    args.height = ImageSizeUnit(args.height)

    # Validate the format is a valid image format
    try:
        args.format = ImageFormat[args.format.upper()]
    except KeyError:
        raise ValueError("Invalid image format")

    return args
