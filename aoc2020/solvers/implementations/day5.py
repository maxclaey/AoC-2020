import logging
import re
from pathlib import Path
from typing import List, Optional

from aoc2020.solvers import PuzzleSolver, SolverFactory

logger = logging.getLogger("SolverDay5")


@SolverFactory.register(day=5)
class SolverDay5(PuzzleSolver):
    def __init__(self, input_file: Path):
        super().__init__(input_file=input_file)

    @property
    def demo_result_1(self) -> Optional[int]:
        return 820

    @property
    def demo_result_2(self) -> Optional[int]:
        return None

    def _read_file(self) -> List[int]:
        seat_ids: List[int] = []
        pattern = "^[F|B]{7}[L|R]{3}$"
        for line in self._input_file.open(mode="r"):
            line = line.strip()
            if re.fullmatch(pattern, line) is not None:
                binary = line.replace("F", "0").replace("B", "1").replace("L", "0").replace("R", "1")
                seat_id = int(binary, 2)
                logger.debug(f"Decoded seat ID is {seat_id}")
                seat_ids.append(seat_id)
            else:
                logger.error(f"Invalid pass detected: {line}")
        return seat_ids

    def solve_1(self) -> int:
        return max(self._input_data)

    def solve_2(self) -> int:
        max_id = max(self._input_data)
        # Get all seat numbers
        all_seats = set(range(max_id+1))
        # Get missing seat numbers
        missing_seats = all_seats - set(self._input_data)
        # Find missing seat for which adjacent seats are not missing
        for seat in missing_seats:
            if seat-1 not in missing_seats and seat+1 not in missing_seats:
                return seat
        logger.error(f"No solution found")
        return 0
