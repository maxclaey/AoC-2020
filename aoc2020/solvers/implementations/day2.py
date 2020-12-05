import logging
import re
from pathlib import Path
from typing import List, Optional, Tuple

from aoc2020.solvers import PuzzleSolver, SolverFactory

logger = logging.getLogger("SolverDay2")


@SolverFactory.register(day=2)
class SolverDay2(PuzzleSolver):

    def __init__(self, input_file: Path):
        super().__init__(input_file=input_file)

    def _read_file(self) -> List[Tuple[int, int, str, str]]:
        regex = "([0-9]+)-([0-9]+) (.): (.*)"
        values = []
        with self._input_file.open(mode="r") as f:
            for line in f:
                result = re.fullmatch(regex, line.strip())
                if result is None:
                    logger.error(f'Could not match line {line}')
                    continue
                int_1 = int(result.group(1))
                int_2 = int(result.group(2))
                char = result.group(3)
                pwd = result.group(4)
                values.append((int_1, int_2, char, pwd))
        return values

    @property
    def demo_result_1(self) -> Optional[int]:
        return 2

    @property
    def demo_result_2(self) -> Optional[int]:
        return 1

    def solve_1(self) -> int:
        num_valids = 0
        for min_count, max_count, char, pwd in self._input_data:
            if min_count <= pwd.count(char) <= max_count:
                num_valids += 1
        return num_valids

    def solve_2(self) -> int:
        num_valids = 0
        for pos_1, pos_2, char, pwd in self._input_data:
            pos_1 -= 1
            pos_2 -= 1
            if pos_1 < 0 or pos_2 < 0 or pos_1 >= len(pwd) or pos_2 >= len(pwd):
                logger.error(f"Invalid position identifiers {pos_1}-{pos_2}")
                continue
            if (pwd[pos_1] == char) != (pwd[pos_2] == char):
                num_valids += 1
        return num_valids
