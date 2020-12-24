import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set

from aoc2020.solvers import PuzzleSolver, SolverFactory

logger = logging.getLogger("SolverDay24")


@SolverFactory.register(day=24)
class SolverDay24(PuzzleSolver):
    def __init__(self, input_file: Path):
        super().__init__(input_file=input_file)
        self.steps: Dict[str, Tuple[int, int]] = {
            "e": (2, 0), "w": (-2, 0),
            "se": (1, 1), "sw": (-1, 1),
            "ne": (1, -1), "nw": (-1, -1),
        }

    @property
    def demo_result_1(self) -> Optional[int]:
        return 10

    @property
    def demo_result_2(self) -> Optional[int]:
        return 2208

    def _read_file(self) -> List[List[str]]:
        lines: List[List[str]] = []
        with open(self._input_file, mode="r") as f:
            for line in f:
                lines.append(self._parse_line(line.strip()))
        return lines

    @staticmethod
    def _parse_line(line: str) -> List[str]:
        steps: List[str] = []
        while len(line) > 0:
            chars = 1 if line[0] in ["e", "w"] else 2
            steps.append(line[:chars])
            line = line[chars:]
        return steps

    def _get_pos(self, steps: List[str]) -> Tuple[int, int]:
        pos: Tuple[int, int] = (0, 0)
        for step in steps:
            direction: Tuple[int, int] = self.steps[step]
            pos = (pos[0]+direction[0], pos[1]+direction[1])
        return pos

    def _get_black_tiles(self) -> Set[Tuple[int, int]]:
        blacks: Set[Tuple[int, int]] = set()
        for steps in self._input_data:
            tile = self._get_pos(steps=steps)
            # Toggle state
            if tile in blacks:
                blacks.remove(tile)
            else:
                blacks.add(tile)
        return blacks

    def _process_day(
        self, blacks: Set[Tuple[int, int]]
    ) -> Set[Tuple[int, int]]:
        newblacks: Set[Tuple[int, int]] = set()
        tiles = self._get_tiles_and_neighbours(blacks)
        for tile in tiles:
            count = self._count_neighbours(blacks=blacks, pos=tile)
            # When til is black, it stays black when number of black
            #  neighbours is not 0 and not more than 2
            if tile in blacks and 0 < count <= 2:
                newblacks.add(tile)
            # When tile is white, it becomes black when it has exactly
            #  2 black neighbours
            elif tile not in blacks and count == 2:
                newblacks.add(tile)
        return newblacks

    def _get_tiles_and_neighbours(
        self, blacks: Set[Tuple[int, int]]
    ) -> Set[Tuple[int, int]]:
        tiles: Set[Tuple[int, int]] = set()
        # Search all tiles that are adjacent to at least one black tile
        for black in blacks:
            for direction in self.steps.values():
                tile = (black[0]+direction[0], black[1]+direction[1])
                tiles.add(tile)
        return tiles

    def _count_neighbours(
        self,
        blacks: Set[Tuple[int, int]],
        pos: Tuple[int, int]
    ) -> int:
        count = 0
        # Loop over all directions
        for direction in self.steps.values():
            npos = (pos[0]+direction[0], pos[1]+direction[1])
            if npos in blacks:
                count += 1
        return count

    def solve_1(self) -> int:
        blacks = self._get_black_tiles()
        return len(blacks)

    def solve_2(self) -> int:
        blacks = self._get_black_tiles()
        for day in range(100):
            blacks = self._process_day(blacks=blacks)
            logger.debug(f"Day {day+1}: {len(blacks)}")
        return len(blacks)
