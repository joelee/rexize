import argparse

from cli import argparser
from icecream import ic


def parse_args():
    parser = argparse.ArgumentParser(
        description="Bulk resize and convert images from a folder recursively."
    )
    parser.add_argument("input_folder", type=str, help="Input folder containing images")
    parser.add_argument(
        "output_folder", type=str, help="Output folder for resized images"
    )
    parser.add_argument(
        "-W", "--width", type=str, default="0", help="Width to resize the image"
    )
    parser.add_argument(
        "-H", "--height", type=str, default="0", help="Height to resize the image"
    )
    parser.add_argument(
        "-f", "--format", type=str, default="WEBP", help="Format of the output image"
    )
    return parser.parse_args()


def main():
    args = argparser()
    ic(args)


if __name__ == "__main__":
    main()
