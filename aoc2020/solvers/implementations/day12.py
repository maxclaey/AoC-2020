import logging
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np

from aoc2020.solvers import PuzzleSolver, SolverFactory

logger = logging.getLogger("SolverDay12")


@SolverFactory.register(day=12)
class SolverDay12(PuzzleSolver):
    def __init__(self, input_file: Path):
        super().__init__(input_file=input_file)
        self._compass: Dict[str, Tuple[int, int]] = {
            "N": (0, 1), "S": (0, -1), "E": (1, 0), "W": (-1, 0),
        }
        self._rotation: Dict[str, int] = {"R": 1, "L": -1}

    @property
    def demo_result_1(self) -> Optional[int]:
        return 25

    @property
    def demo_result_2(self) -> Optional[int]:
        return 286

    def _read_file(self) -> List[Tuple[str, int]]:
        instructions: List[Tuple[str, int]] = []
        with self._input_file.open(mode="r") as f:
            for line in f:
                line = line.strip()
                try:
                    direction = line[0]
                    amount = int(line[1:])
                    instructions.append((direction, amount))
                except ValueError:
                    logger.error(f"Invalid input line {line}")
        return instructions

    @staticmethod
    @lru_cache(maxsize=32)
    def _rotation_matrix(degrees: int) -> np.ndarray:
        sin = np.sin(np.radians(degrees))
        cos = np.cos(np.radians(degrees))
        return np.array([[cos, -sin], [sin, cos]])

    @staticmethod
    def _rotate(
        pos: Tuple[int, int], direction: int, amount: int
    ) -> Tuple[int, int]:
        degrees = direction * amount
        rot_mat = SolverDay12._rotation_matrix(degrees=degrees)
        result = np.rint(np.dot(pos, rot_mat)).astype(np.int)
        return result[0], result[1]

    @staticmethod
    def _move(
        pos: Tuple[int, int], direction: Tuple[int, int], amount: int
    ) -> Tuple[int, int]:
        x = pos[0] + direction[0]*amount
        y = pos[1] + direction[1]*amount
        return x, y

    def solve_1(self) -> int:
        orientation = (1, 0)  # East
        pos = (0, 0)

        for direction, amount in self._input_data:
            if direction in self._compass:
                pos = self._move(
                    pos=pos,
                    direction=self._compass[direction],
                    amount=amount,
                )
            elif direction in self._rotation:
                orientation = self._rotate(
                    pos=orientation,
                    direction=self._rotation[direction],
                    amount=amount,
                )
            elif direction == "F":
                pos = self._move(
                    pos=pos, direction=orientation, amount=amount
                )
            else:
                logger.warning(f"Invalid direction {direction}")
        return abs(pos[0]) + abs(pos[1])

    def solve_2(self) -> int:
        waypoint = (10, 1)
        pos = (0, 0)

        for direction, amount in self._input_data:
            if direction in self._compass:
                waypoint = self._move(
                    pos=waypoint,
                    direction=self._compass[direction],
                    amount=amount,
                )
            elif direction in self._rotation:
                waypoint = self._rotate(
                    pos=waypoint,
                    direction=self._rotation[direction],
                    amount=amount,
                )
            elif direction == "F":
                pos = self._move(pos=pos, direction=waypoint, amount=amount)
            else:
                logger.warning(f"Invalid direction {direction}")
        return abs(pos[0]) + abs(pos[1])
