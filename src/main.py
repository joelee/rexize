#!/usr/bin/env python3
import os
import sys
import traceback

from console import ConsoleLevel, console

sys.path.append(os.path.dirname(__file__))

from cli import CLI  # noqa: E402
from extension_manager import ExtensionManager  # noqa: E402
from file_iterator import FileIterator  # noqa: E402
from image_manipulator import ImageManipulator  # noqa: E402


class Rexize:
    SUPPORTED_FORMATS = ["jpeg", "png", "webp", "gif", "tiff", "bmp"]

    def __init__(self):
        try:
            # Parse the command line arguments
            cli = CLI().parse_args().validate_args()

            # Set the console log level
            if cli.args.quiet:
                console.set_level(ConsoleLevel.ERROR)
            if cli.args.verbose:
                console.set_level(ConsoleLevel.VERBOSE)
            if bool(os.environ.get("DEV_MODE")):
                console.set_level(ConsoleLevel.DEBUG)
                console.print("Running in Development mode")

            console.debug(f"Input arguments: {cli.args}")

            self._cli = cli
            self._ext_manager = ExtensionManager()
            self._file_count = 0
            self._finalise_processes = []
        except Exception as e:
            console.exception(e)
            sys.exit(55)

    @property
    def args(self):
        return self._cli.args

    def run(self):
        try:
            if self.args.list_extensions:
                self.list_extensions_and_exit()
            self.process_images()
            if self._finalise_processes:
                self.finalise_images()
            sys.exit(0)
        except Exception as e:
            console.exception(e)
            console.debug(traceback.format_exc())
            sys.exit(1)

    def process_images(self):
        # Process the images in the input folder
        for file in self._input_iterator().walk():
            image = ImageManipulator(file)

            # Pre-process the image
            if self.args.pre_processor:
                for extension_name in self.args.pre_processor:
                    self.apply_extension(extension_name, image)

            image.resize(self.args.width, self.args.height, self.args.max_size)

            # Post-process the image
            if self.args.post_processor:
                for extension_name in self.args.post_processor:
                    self.apply_extension(extension_name, image)

            out_file = self.get_output_file(file, self.args)
            console.print(f"Processing: {file} --> {out_file}")
            self._file_count += 1
            image.save(out_file)
        console.print(f"Processed {self._file_count} files.")

    def finalise_images(self):
        final_count = 0
        for file in self._output_iterator().walk():
            image = ImageManipulator(file)
            for extension_name in self._finalise_processes:
                self.apply_extension(extension_name, image)
            final_count += 1
            image.save(file)
        console.print(f"Finalised {final_count} files.")
        if final_count != self._file_count:
            console.error(
                f"Finalised {final_count} files do not match "
                f"{self._file_count} processed files."
            )

    def apply_extension(self, extension_name: str, image: ImageManipulator):
        ext = self._ext_manager.get(extension_name)
        ext.apply(image.image)
        if ext.has_finaliser():
            self._finalise_processes.append(ext)

    def list_extensions_and_exit(self):
        # List the available extensions and exit
        console.set_level(ConsoleLevel.INFO)
        console.print(
            "Available Extensions (Use with the pre and post processor options):"
        )
        for ext_name, ext_desc in self._ext_manager.list_extensions().items():
            console.print(f"  {ext_name}: {ext_desc}")
        sys.exit(0)

    def _input_iterator(self):
        return FileIterator(self.args.input_folder).filter_by_extension(
            self.SUPPORTED_FORMATS
        )

    def _output_iterator(self):
        return FileIterator(self.args.output_folder).filter_by_extension(
            self.SUPPORTED_FORMATS
        )

    def _get_output_file(self, file: str) -> str:
        base_dir = self.args.output_folder
        if base_dir.endswith("/"):
            base_dir = base_dir[:-1]

        if file.startswith(self.args.input_folder):
            file = file[len(self.args.input_folder) :]
            if file.startswith("/"):
                file = file[1:]

        file = f"{base_dir}/{file}"
        name, ext = os.path.splitext(file)

        # replace file extension with the new format
        new_ext = self.args.format.value.lower()
        if new_ext == "jpeg":
            new_ext = "jpg"

        new_file = f"{name}.{new_ext}" if len(ext) < 5 else f"{file}.{new_ext}"

        dir_name = os.path.dirname(new_file)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        return new_file


if __name__ == "__main__":
    Rexize().run()
