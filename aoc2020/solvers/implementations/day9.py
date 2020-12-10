import logging
from collections import deque
from pathlib import Path
from typing import Deque, List, Optional

from aoc2020.solvers import PuzzleSolver, SolverFactory

logger = logging.getLogger("SolverDay9")


@SolverFactory.register(day=9)
class SolverDay9(PuzzleSolver):
    def __init__(self, input_file: Path):
        super().__init__(input_file=input_file)

    @property
    def demo_result_1(self) -> Optional[int]:
        return 127

    @property
    def demo_result_2(self) -> Optional[int]:
        return 62

    def _read_file(self) -> List[int]:
        values: List[int] = []
        with self._input_file.open(mode="r") as f:
            for line in f:
                try:
                    val = int(line.strip())
                    values.append(val)
                except ValueError:
                    logger.error(f"Line {line} is not a valid number")
                    continue
        return values

    @classmethod
    def _is_sum(cls, values: List[int], value: int) -> bool:
        for val in values:
            remainder = value - val
            if remainder in values:
                if remainder != val or values.count(val) > 1:
                    return True
        return False

    def solve_1(self) -> int:
        # Demo uses different preamble size, so check on input length
        if len(self._input_data) == 20:
            preamble_size = 5
        else:
            preamble_size = 25
        prev_numbers: Deque[int] = deque(maxlen=preamble_size)
        for value in self._input_data:
            if len(prev_numbers) == preamble_size:
                if not self._is_sum(values=list(prev_numbers), value=value):
                    logger.debug(
                        f"Found solution: {value} is not a sum of the "
                        f"previous {preamble_size} values."
                    )
                    return value
            prev_numbers.append(value)
        logger.error(f"No solution found to puzzle 1")
        return 0

    def solve_2(self) -> int:
        target = self.solve_1()
        for i in range(len(self._input_data)):
            sum_values = []
            for j in range(i, len(self._input_data)):
                sum_values.append(self._input_data[j])
                if sum(sum_values) == target and len(sum_values) > 2:
                    logger.debug(
                        f"Found solution: values "
                        f"{','.join(map(str, sum_values))} sum to {target}."
                    )
                    return min(sum_values) + max(sum_values)
                elif sum(sum_values) > target:
                    break
        logger.error(f"No solution found to puzzle 1")
        return 0
