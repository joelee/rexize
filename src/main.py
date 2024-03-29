#!/usr/bin/env python3

import os
import sys
import traceback

sys.path.append(os.path.dirname(__file__))

from cli import CLI  # noqa: E402
from file_iterator import FileIterator  # noqa: E402
from image_manipulator import ImageManipulator  # noqa: E402


def main():
    try:
        cli = CLI().parse_args().validate_args()

        file_iter = FileIterator(cli.args.input_folder).filter_by_extension(
            ["jpg", "jpeg", "png", "webp", "gif", "tiff", "bmp"]
        )
        file_count = 0
        for file in file_iter.walk():
            image = ImageManipulator(file)
            cli.debug(f"Processing: {cli.args}")
            image.resize(cli.args.width, cli.args.height, cli.args.max_size)
            if cli.args.rgb:
                image.downscale_to_rgb()
            if cli.args.grayscale:
                image.downscale_to_grayscale()

            out_file = get_output_file(file, cli.args)
            cli.print(f"{file} --> {out_file}")
            file_count += 1
            image.save(out_file)

        cli.print(f"Processed {file_count} files.")
        cli.exit()

    except Exception as e:
        cli.exception(e)
        cli.debug(traceback.format_exc())
        cli.exit(1)


def get_output_file(file: str, args) -> str:
    base_dir = args.output_folder
    if base_dir.endswith("/"):
        base_dir = base_dir[:-1]

    if file.startswith(args.input_folder):
        file = file[len(args.input_folder) :]
        if file.startswith("/"):
            file = file[1:]

    file = f"{base_dir}/{file}"
    name, ext = os.path.splitext(file)

    # replace file extension with the new format
    new_ext = args.format.value.lower()
    if new_ext == "jpeg":
        new_ext = "jpg"

    new_file = f"{name}.{new_ext}" if len(ext) < 5 else f"{file}.{new_ext}"

    dir_name = os.path.dirname(new_file)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    return new_file


if __name__ == "__main__":
    main()
