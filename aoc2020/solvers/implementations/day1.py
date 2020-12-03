import logging
from collections import defaultdict
from pathlib import Path
from typing import List

from aoc2020.solvers import PuzzleSolver, SolverFactory

logger = logging.getLogger("SolverDay1")


@SolverFactory.register(day=1)
class SolverDay1(PuzzleSolver):

    def __init__(self, input_file: Path):
        super().__init__(input_file=input_file)

    @property
    def demo_result_1(self) -> int:
        return 514579

    @property
    def demo_result_2(self) -> int:
        return 241861950

    def _read_file(self) -> List[int]:
        with self._input_file.open(mode="r") as f:
            values = list(map(int, [l for l in f]))
        return values

    def solve_1(self) -> int:
        # Count the occurrences of each value
        value_occ = defaultdict(int)
        for val in self._input_data:
            value_occ[val] += 1
        # Loop over unique values to check solution
        for value, count in value_occ.items():
            # Edge case 1010
            if value == 1010:
                if count > 1:
                    logger.debug(f"Values are {value} and {value}")
                    return 1010*1010
            else:
                if 2020-value in value_occ:
                    logger.debug(f"Values are {value} and {2020-value}")
                    return value * (2020-value)
        logger.error(f"Solution not found")
        return -1

    def solve_2(self) -> int:
        # Get all unique sums of 2 values, and how they are composed
        sums = defaultdict(list)
        for i, val1 in enumerate(self._input_data):
            for j, val2 in enumerate(self._input_data):
                if i != j:
                    sums[val1+val2].append((i, j))
        for i, val in enumerate(self._input_data):
            rem = 2020 - val
            for indices in sums[rem]:
                if i not in indices:
                    logger.info(
                        f"Values are {self._input_data[indices[0]]}, "
                        f"{self._input_data[indices[1]]} and {val}"
                    )
                    return self._input_data[indices[0]]*self._input_data[indices[1]]*val
        logger.error(f"Solution not found")
        return -1
