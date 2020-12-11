import logging
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

import numpy as np

from aoc2020.solvers import PuzzleSolver, SolverFactory

logger = logging.getLogger("SolverDay11")


@SolverFactory.register(day=11)
class SolverDay11(PuzzleSolver):
    def __init__(self, input_file: Path):
        super().__init__(input_file=input_file)
        self._search_domains: Dict[Tuple[int, int], List[List[Tuple[int, int]]]] = {}
        self._create_search_domains()

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

    def _occupied_closest_neighbours(
        self, state: np.ndarray, row: int, col: int
    ) -> int:
        occupied: int = 0
        for domain in self._search_domains[(row, col)]:
            for r, c in domain:
                if state[r][c] < 0:
                    continue
                occupied += state[r][c]
                break

        return occupied

    def _create_search_domains(self) -> None:
        for row in range(self._input_data.shape[0]):
            for col in range(self._input_data.shape[1]):
                # Define motion room
                up_room: int = row+1
                down_room: int = self._input_data.shape[0]-row
                left_room: int = col+1
                right_room: int = self._input_data.shape[1]-col
                self._search_domains[(row, col)] = [
                    [(row-i, col) for i in range(1, up_room)],  # Up
                    [(row+i, col) for i in range(1, down_room)],  # Down
                    [(row, col-i) for i in range(1, left_room)],  # Left
                    [(row, col+i) for i in range(1, right_room)],  # Right
                    [(row-i, col-i) for i in range(1, min(up_room, left_room))],  # Up-left
                    [(row+i, col+i) for i in range(1, min(down_room, right_room))],  # Down-right
                    [(row-i, col+i) for i in range(1, min(up_room, right_room))],  # Up-right
                    [(row+i, col-i) for i in range(1, min(down_room, left_room))],  # Down-left
                ]

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
                occ_fn=self._occupied_closest_neighbours,
                margin=5,
            )
            if np.array_equal(state, new_state):
                return int(np.sum(np.maximum(new_state, 0)))
            state = new_state
