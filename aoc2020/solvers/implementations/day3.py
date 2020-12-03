import logging
from pathlib import Path

import numpy as np

from aoc2020.solvers import PuzzleSolver, SolverFactory

logger = logging.getLogger("SolverDay3")


@SolverFactory.register(day=3)
class SolverDay3(PuzzleSolver):
    def __init__(self, input_file: Path):
        super().__init__(input_file=input_file)

    @property
    def demo_result_1(self) -> int:
        return 7

    @property
    def demo_result_2(self) -> int:
        return 336

    def _read_file(self) -> np.ndarray:
        rows = []
        with self._input_file.open(mode='r') as f:
            for line in f:
                line = line.strip()
                # Check for illegal characters in the rows
                if line.count(".") + line.count("#") != len(line):
                    logger.error(f"Line '{line}' contains illegal characters")
                    continue
                rows.append([int(c == "#") for c in line])
        return np.array(rows)

    def _count_trees(self, right: int, down: int) -> int:
        n_rows, n_cols = self._input_data.shape
        trees = 0
        for i, row in enumerate(range(0, n_rows, down)):
            col = (i * right) % n_cols
            trees += self._input_data[row, col]
        logger.debug(
            f"Number of trees for slope {right} right, {down }down: {trees}"
        )
        return trees

    def solve_1(self) -> int:
        return self._count_trees(right=3, down=1)

    def solve_2(self) -> int:
        slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
        result = 1
        for right, down in slopes:
            res = self._count_trees(right=right, down=down)
            result *= res
        return result
