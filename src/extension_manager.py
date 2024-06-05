import glob
import importlib.util
import os
import sys

from base_extension import BaseExtension
from icecream import ic
from PIL import Image


class ExtensionManager:
    PREFIX = "rexize_ext_"  # Prefix for external extension modules
    EXT_CLASS_NAME = "RexizeExtension"
    EXT_PATH = os.path.join(os.path.dirname(__file__), "extension")

    def __init__(self):
        self._extensions = {}

    def get(self, extension_name):
        ext = self._load_extension(extension_name)
        if isinstance(ext, BaseExtension):
            return ext
        raise TypeError(f"{extension_name} is NOT a Rexize Extension")

    def apply(self, extension_name, image: Image.Image):
        extension = self._load_extension(extension_name)
        return extension.apply(image)

    def finalise(self, extension_name, image: Image.Image):
        extension = self._load_extension(extension_name)
        return extension.finalise(image)

    def register(self, extension_name, extension_instance):
        if not isinstance(extension_instance, BaseExtension):
            raise TypeError("Extension must be of type BaseExtension")
        if extension_name in self._extensions:
            raise ValueError(f"Extension '{extension_name}' already registered")
        self._extensions[extension_name] = extension_instance

    def list_extensions(self):
        """
        List all available extensions in the extension directory.
        :return:
        """
        extensions = {}
        ic(self.EXT_PATH)
        for ext_file in glob.glob(f"{self.EXT_PATH}/*.py"):
            ic(ext_file)
            ext_name = os.path.basename(ext_file)[:-3]
            if ext_name.startswith("__"):
                continue
            ext_instance = self._load_extension(ext_name)
            extensions[ext_name] = ext_instance.about()
        return extensions

    def _load_extension(self, extension_name):
        if extension_name in self._extensions:
            return self._extensions[extension_name]

        try:
            module_name = f"{self.PREFIX}{extension_name}"
            spec = importlib.util.spec_from_file_location(
                module_name, f"{self.EXT_PATH}/{extension_name}.py"
            )
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            if not hasattr(module, self.EXT_CLASS_NAME):
                raise ImportError(
                    f"Extension '{extension_name}' is not a Rexize Extension"
                )
            self._extensions[extension_name] = module.RexizeExtension()
            return self._extensions[extension_name]
        except ModuleNotFoundError as e:
            raise ImportError(f"Extension '{extension_name}' not found") from e


if __name__ == "__main__":
    print("Extension Manager")
    em = ExtensionManager()
    ic(em.list_extensions())
