import pkg_resources
from pathlib import Path


class DataFactory:

    @classmethod
    def get_demo_file(cls, day: int) -> Path:
        target = f"demo_files/day{day}.txt"
        return Path(pkg_resources.resource_filename(__package__, target))

    @classmethod
    def get_input_file(cls, day: int) -> Path:
        target = f"input_files/day{day}.txt"
        return Path(pkg_resources.resource_filename(__package__, target))
