import argparse
import os
import sys

from icecream import ic

from image import ImageFormat, ImageSizeUnit


class CLI:
    DEFAULT_CLI_ARGS = ["/tmp", "/tmp"]

    def __init__(self, cli_args=None, debug_mode: bool = False) -> None:
        self._args = None
        self._dev_mode = debug_mode or bool(os.environ.get("DEV_MODE"))
        if cli_args:
            self.parse_args(cli_args)

    def parse_args(self, cli_args=None):
        self._args = self._argparser(cli_args)
        if self._dev_mode:
            ic(self._args)
        return self.validate_args()

    @property
    def args(self) -> argparse.Namespace:
        if not self._args:
            self._args = self._argparser(self.DEFAULT_CLI_ARGS)
        return self._args

    def print(self, *args, **kwargs):
        if not self.args.quiet:
            print(*args, **kwargs)

    def error(self, *args, **kwargs):
        print(*args, file=sys.stderr, **kwargs)

    def exception(self, error: Exception):
        self.error(error)
        if self._dev_mode:
            ic(error)

    def verbose(self, *args, **kwargs):
        if self.args.verbose:
            print(*args, **kwargs)

    def debug(self, *args, **kwargs):
        if self._dev_mode:
            ic(*args, **kwargs)

    def exit(self, status: int = 0):
        sys.exit(status)

    def validate_args(self):
        if not self.args.input_folder:
            raise ValueError("Input folder is required")
        if not self.args.width and not self.args.height and not self.args.max_size:
            raise ValueError("At least one of width, height or max-size is required")

        # Validate the input folder exists and readable
        if not os.path.isdir(self.args.input_folder) or not os.access(
            self.args.input_folder, os.R_OK
        ):
            raise FileNotFoundError(
                f"Input folder not found or readable at {self.args.input_folder}"
            )

        # Build output_folder from input_folder if not provided
        if not self.args.output_folder:
            self.args.output_folder = f"{self.args.input_folder}_resized"

        # Create the output folder if not exists and check if writable
        if not os.path.exists(self.args.output_folder):
            os.makedirs(self.args.output_folder)
        if not os.access(self.args.output_folder, os.W_OK):
            raise PermissionError(
                f"Output folder not writable at {self.args.output_folder}"
            )

        return self

    @staticmethod
    def _argparser(cli_args=None) -> argparse.Namespace:
        parser = argparse.ArgumentParser(
            description="Bulk resize and convert images from a folder recursively."
        )
        parser.add_argument(
            "input_folder",
            type=str,
            default="/tmp",
            help="Input folder containing images",
        )
        parser.add_argument(
            "output_folder",
            type=str,
            default="/tmp",
            help="Output folder for resized images",
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
            "-M",
            "--max-size",
            type=int,
            default=0,
            help="Maximum size in pixels for the image. Resize if larger than this size",
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

        args = parser.parse_args(cli_args)

        # Validate the width and height
        args.width = ImageSizeUnit(args.width)
        args.height = ImageSizeUnit(args.height)

        args.max_size = ImageSizeUnit(args.max_size)

        # Validate the format is a valid image format
        try:
            args.format = ImageFormat[args.format.upper()]
        except KeyError:
            raise ValueError("Invalid image format")

        return args
