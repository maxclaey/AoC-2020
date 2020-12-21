from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Optional, Union


class PuzzleSolver(ABC):
    def __init__(self, input_file: Path):
        self._input_file = input_file
        self._input_data = self._read_file()

    # ABSTRACT PROPERTIES
    @property
    @abstractmethod
    def demo_result_1(self) -> Optional[Union[int, str]]:
        raise NotImplementedError

    @property
    @abstractmethod
    def demo_result_2(self) -> Optional[Union[int, str]]:
        raise NotImplementedError

    # ABSTRACT SOLVER METHODS
    @abstractmethod
    def _read_file(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def solve_1(self) -> Union[int, str]:
        raise NotImplementedError

    @abstractmethod
    def solve_2(self) -> Union[int, str]:
        raise NotImplementedError
