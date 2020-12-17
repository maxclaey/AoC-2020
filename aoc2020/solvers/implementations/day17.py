import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np

from aoc2020.solvers import PuzzleSolver, SolverFactory

logger = logging.getLogger("SolverDay17")


@SolverFactory.register(day=17)
class SolverDay17(PuzzleSolver):
    def __init__(self, input_file: Path):
        super().__init__(input_file=input_file)

    @property
    def demo_result_1(self) -> Optional[int]:
        return 112

    @property
    def demo_result_2(self) -> Optional[int]:
        return 848

    def _read_file(self) -> List[List[bool]]:
        mapping: Dict[str, bool] = {".": False, "#": True}
        lines: List[List[bool]] = []
        size = 0
        with self._input_file.open(mode="r") as f:
            for line in f:
                line = line.strip()
                try:
                    values: List[bool] = list(map(lambda x: mapping[x], line))
                except KeyError:
                    logger.error(f"Failed to parse line {line}")
                    continue
                if size == 0:
                    size = len(values)
                elif size != len(values):
                    logger.error(
                        f"Invalid line contains {len(values)} values "
                        f"instead of {size}"
                    )
                    continue
                lines.append(values)
        if len(lines) != size:
            logger.error(
                f"Number of lines {len(line)} differs from number of "
                f"columns {size}"
            )
            return []
        return lines

    @staticmethod
    def _run_cycle(grid: np.ndarray, nh_size: int) -> np.ndarray:
        new_grid = np.copy(grid)
        for index, active in np.ndenumerate(grid):
            active_neighbours = SolverDay17._get_active_neighbours(
                grid=grid, index=index, nh_size=nh_size
            )
            if active:
                new_grid[index] = active_neighbours in [2, 3]
            else:
                new_grid[index] = active_neighbours == 3
        return new_grid

    @staticmethod
    def _get_active_neighbours(
        grid: np.ndarray, index: Tuple[int, ...], nh_size: int
    ) -> int:
        nh_slice = tuple([
            slice(max(0, idx - nh_size), idx + nh_size + 1)
            for idx in index
        ])
        return int(np.sum(grid[nh_slice])) - int(grid[index])

    def solve(self, cycles: int, dimensions: int, nh_size: int = 1) -> int:
        grid = np.array(self._input_data)
        # Go from 2D to requested number of dimensions
        while len(grid.shape) != dimensions:
            grid = np.expand_dims(grid, axis=-1)
        for cycle in range(cycles):
            # Gradually expand the grid to avoid too much computation
            grid = np.pad(grid, nh_size)
            # Run a cycle
            grid = self._run_cycle(grid=grid, nh_size=nh_size)
        return int(np.sum(grid))

    def solve_1(self) -> int:
        cycles = 6
        dimensions = 3
        return self.solve(cycles=cycles, dimensions=dimensions)

    def solve_2(self) -> int:
        cycles = 6
        dimensions = 4
        return self.solve(cycles=cycles, dimensions=dimensions)
