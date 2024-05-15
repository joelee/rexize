import sys
from enum import Enum


class ConsoleLevel(Enum):
    ERROR = 0
    WARNING = 1
    INFO = 2
    VERBOSE = 3
    DEBUG = 4


def console_level(level: ConsoleLevel):
    """
    Decorator to set the level of the console output
    """

    def decorator(func):
        def wrapper(self, *args, **kwargs):
            if self._level.value >= level.value:
                return func(self, *args, **kwargs)

        return wrapper

    return decorator


class Console:
    def __init__(self) -> None:
        self._level = ConsoleLevel.INFO

    def set_level(self, level: ConsoleLevel):
        self._level = level
        return self

    @console_level(ConsoleLevel.INFO)
    def print(self, *args, **kwargs):
        print(*args, **kwargs)

    @console_level(ConsoleLevel.ERROR)
    def error(self, *args, **kwargs):
        print(*args, file=sys.stderr, **kwargs)

    @console_level(ConsoleLevel.ERROR)
    def exception(self, error: Exception):
        self.error(error)
        if self._level.value >= ConsoleLevel.DEBUG.value:
            print(error)

    @console_level(ConsoleLevel.VERBOSE)
    def verbose(self, *args, **kwargs):
        print(*args, **kwargs)

    @console_level(ConsoleLevel.DEBUG)
    def debug(self, *args, **kwargs):
        print(*args, **kwargs)


console = Console()
console.print("\nRexize: Bulk image processor\n")


def get_console() -> Console:
    return console
