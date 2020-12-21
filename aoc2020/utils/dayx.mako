import logging
from pathlib import Path
from typing import Any, Optional

from aoc2020.solvers import PuzzleSolver, SolverFactory

logger = logging.getLogger("SolverDay${day}")


@SolverFactory.register(day=${day})
class SolverDay${day}(PuzzleSolver):
    def __init__(self, input_file: Path):
        super().__init__(input_file=input_file)

    @property
    def demo_result_1(self) -> Optional[int]:
        return None

    @property
    def demo_result_2(self) -> Optional[int]:
        return None

    def _read_file(self) -> Any:
        with open(self._input_file, mode="r") as f:
            for line in f:
                line = line.strip()

    def solve_1(self) -> int:
        logger.warning(f"Solution for puzzle 1 for day ${day} not implemented yet")
        return 0

    def solve_2(self) -> int:
        logger.warning(f"Solution for puzzle 2 for day ${day} not implemented yet")
        return 0
