import logging
from collections import defaultdict, deque
from pathlib import Path
from typing import Deque, Dict, List, Optional

from aoc2020.solvers import PuzzleSolver, SolverFactory

logger = logging.getLogger("SolverDay15")


@SolverFactory.register(day=15)
class SolverDay15(PuzzleSolver):
    def __init__(self, input_file: Path):
        super().__init__(input_file=input_file)

    @property
    def demo_result_1(self) -> Optional[int]:
        return 436

    @property
    def demo_result_2(self) -> Optional[int]:
        return 175594

    def _read_file(self) -> List[int]:
        with self._input_file.open(mode="r") as f:
            lines = [l.strip() for l in f]
            if len(lines) != 1:
                logger.error(f"Invalid input, found {len(lines)}, expected 1")
                return []
            try:
                turns = list(map(int, lines[0].split(",")))
                return turns
            except ValueError:
                logger.error(f"Failed to parse input lines")
                return []

    def _find_value(self, turn: int) -> int:
        turns = self._input_data
        occurences: Dict[int, Deque] = defaultdict(lambda: deque(maxlen=2))
        last_value = 0
        for i in range(turn):
            if i < len(turns):
                value = turns[i]
            else:
                occ = occurences[last_value]
                if len(occ) < 2:
                    value = 0
                else:
                    value = occ[0] - occ[1]
            occurences[value].appendleft(i+1)  # Turns are 1-indexed
            last_value = value
        return last_value

    def solve_1(self) -> int:
        return self._find_value(turn=2020)

    def solve_2(self) -> int:
        return self._find_value(turn=30000000)
