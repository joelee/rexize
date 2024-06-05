import argparse
import json
import os

import yaml
from console import console
from image import ImageFormat, ImageSizeUnit


class CLI:
    DEFAULT_CLI_ARGS = ["-h"]

    def __init__(self, cli_args=None) -> None:
        self._args = None
        if cli_args:
            self.parse_args(cli_args)

    def parse_args(self, cli_args=None):
        self._args = self._argparser(cli_args)
        console.verbose(f"Input Args: {self._args}")
        if self._args.list_extensions:
            self.list_extensions_and_exit()
        return self.validate_args()

    @property
    def args(self) -> argparse.Namespace:
        if not self._args:
            self._args = self._argparser(self.DEFAULT_CLI_ARGS)
        return self._args

    def validate_args(self):
        # if self.args.config:
        #     self.read_config(self.args.config)
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
            "-i",
            "--input_folder",
            type=str,
            help="Input folder containing images",
        )
        parser.add_argument(
            "-o",
            "--output_folder",
            type=str,
            help="Output folder for resized images",
        )
        parser.add_argument(
            "-C",
            "--config",
            type=str,
            default="",
            help="Path to the configuration file.",
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
            help=(
                "Maximum size in pixels for the image. Resize if larger than this size"
            ),
        )
        parser.add_argument(
            "-f",
            "--format",
            type=str,
            default="WEBP",
            help="Format of the output image: JPEG, PNG, WEBP, GIF, TIFF, BMP",
        )
        parser.add_argument(
            "-p",
            "--pre-processor",
            type=str,
            action="append",
            help="Use a pre-processor EXTENSION to process the image before resizing",
        )
        parser.add_argument(
            "-P",
            "--post-processor",
            type=str,
            action="append",
            help="Use a post-processor EXTENSION to process the image after resizing",
        )
        parser.add_argument(
            "-l",
            "--list-extensions",
            action="store_true",
            help="List all available extensions for pre and post processing",
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

        # Load configuration from file if provided
        if args.config:
            with open(args.config) as f:
                if args.config.lower().endswith(".json"):
                    config = json.load(f)
                elif args.config.lower().endswith(".yaml"):
                    config = yaml.safe_load(f)
                else:
                    raise ValueError(
                        f"Configuration file {args.config} is not JSON or YAML"
                    )
            console.verbose(f"Configuration loaded from {args.config}:\n{config}")
            for key in config.keys():
                if key not in vars(args):
                    raise ValueError(f"Invalid configuration key: {key}")
                setattr(args, key, config[key])

        # Validate the width and height
        args.width = ImageSizeUnit(args.width)
        args.height = ImageSizeUnit(args.height)

        args.max_size = ImageSizeUnit(args.max_size)

        # Validate the format is a valid image format
        try:
            args.format = ImageFormat[args.format.upper()]
        except KeyError as e:
            raise ValueError("Invalid image format") from e

        return args
