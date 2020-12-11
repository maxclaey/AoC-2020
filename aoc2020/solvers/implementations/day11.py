import logging
from pathlib import Path
from typing import Callable, List, Optional

import numpy as np

from aoc2020.solvers import PuzzleSolver, SolverFactory

logger = logging.getLogger("SolverDay11")


@SolverFactory.register(day=11)
class SolverDay11(PuzzleSolver):
    def __init__(self, input_file: Path):
        super().__init__(input_file=input_file)

    @property
    def demo_result_1(self) -> Optional[int]:
        return 37

    @property
    def demo_result_2(self) -> Optional[int]:
        return 26

    def _read_file(self) -> np.ndarray:
        mapping = {".": -1, "L": 0, "#": 1}
        data: List[List[int]] = []
        with open(self._input_file, mode="r") as f:
            for line in f:
                line = line.strip()
                row: List[int] = []
                for c in line:
                    val = mapping.get(c)
                    if val is None:
                        logger.error(f"Invalid line: {line}")
                        row = []
                        break
                    row.append(val)
                if len(row) > 0:
                    data.append(row)
        return np.array(data)

    @staticmethod
    def _apply_round(
        state: np.ndarray,
        occ_fn: Callable[[np.ndarray, int, int], int],
        margin: int
    ) -> np.ndarray:
        new_state = np.copy(state)
        for r in range(state.shape[0]):
            for c in range(state.shape[1]):
                val = state[r][c]
                if val < 0:
                    continue
                o_neighbours = occ_fn(state, r, c)
                # When empty and no neighbours: occupy
                if val == 0 and o_neighbours == 0:
                    new_state[r][c] = 1
                # When occupied and too many neighbours: leave
                elif val == 1 and o_neighbours >= margin:
                    new_state[r][c] = 0
        return new_state

    @staticmethod
    def _occupied_adjacent_neighbours(
        state: np.ndarray, row: int, col: int
    ) -> int:
        # Define the adjacency neighbourhood
        neighbourhood = np.maximum(
            state[max(0, row-1):row+2, max(0, col-1):col+2], 0
        )
        # Count occupied neighbours, exclude current position
        return np.sum(neighbourhood) - max(0, state[row][col])

    @staticmethod
    def _occupied_closest_neightbours(
        state: np.ndarray, row: int, col: int
    ) -> int:
        occupied = 0
        # Search UP
        for r in reversed(range(row)):
            if state[r][col] < 0:
                continue
            occupied += state[r][col]
            break
        # Search DOWN
        for r in range(row+1, state.shape[0]):
            if state[r][col] < 0:
                continue
            occupied += state[r][col]
            break
        # Search LEFT
        for c in reversed(range(col)):
            if state[row][c] < 0:
                continue
            occupied += state[row][c]
            break
        # Search RIGHT
        for c in range(col+1, state.shape[1]):
            if state[row][c] < 0:
                continue
            occupied += state[row][c]
            break
        # Search UP-LEFT
        for i in range(1, min(col+1, row+1)):
            if state[row-i][col-i] < 0:
                continue
            occupied += state[row-i][col-i]
            break
        # Search DOWN-RIGHT
        for i in range(1, min(state.shape[0]-row, state.shape[1]-col)):
            if state[row+i][col+i] < 0:
                continue
            occupied += state[row+i][col+i]
            break
        # Search UP-RIGHT
        for i in range(1, min(row+1, state.shape[1]-col)):
            if state[row-i][col+i] < 0:
                continue
            occupied += state[row-i][col+i]
            break
        # Search DOWN-LEFT
        for i in range(1, min(col+1, state.shape[0]-row)):
            if state[row+i][col-i] < 0:
                continue
            occupied += state[row+i][col-i]
            break
        return occupied

    def solve_1(self) -> int:
        state = self._input_data
        while True:
            new_state = self._apply_round(
                state=state,
                occ_fn=self._occupied_adjacent_neighbours,
                margin=4,
            )
            if np.array_equal(state, new_state):
                return int(np.sum(np.maximum(new_state, 0)))
            state = new_state

    def solve_2(self) -> int:
        state = self._input_data
        while True:
            new_state = self._apply_round(
                state=state,
                occ_fn=self._occupied_closest_neightbours,
                margin=5,
            )
            if np.array_equal(state, new_state):
                return int(np.sum(np.maximum(new_state, 0)))
            state = new_state
