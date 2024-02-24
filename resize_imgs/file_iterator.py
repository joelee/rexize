# Iterate through the files in the directory recursively with option to filter by file extensions
# and return a Generator of the file paths.

# Usage:
# for file in file_iterator("path/to/directory").walk():
#     print(file)

import os
from os.path import join, splitext
from typing import Generator, Self


class FileIterator:
    def __init__(self, directory: str) -> None:
        if self._is_valid_directory(directory):
            self._directory = directory
            self._filters: list[callable] = []
        else:
            raise FileNotFoundError(f"Directory not found or readable at {directory}")

    def add_filter(self, filter: callable) -> Self:
        self._filters.append(filter)
        return self

    def filter_by_extension(self, extensions: list[str]) -> Self:
        def filter(file: str) -> bool:
            _, ext = splitext(file)
            return ext[1:] in extensions

        self.add_filter(filter)
        return self

    def walk(self) -> Generator[str, None, None]:
        for root, _, files in os.walk(self._directory):
            for file in files:
                if self._check_filter(file):
                    yield join(root, file)

    def _is_valid_directory(self, directory_path: str) -> bool:
        # check if directory exists and readable
        return os.path.isdir(directory_path) and os.access(directory_path, os.R_OK)

    def _check_filter(self, file: str) -> bool:
        if not self._filters:
            return True
        for filter in self._filters:
            if not filter(file):
                return False
        return True
