import logging
from pathlib import Path
from typing import List, Optional, Set

from aoc2020.solvers import PuzzleSolver, SolverFactory

logger = logging.getLogger("SolverDay6")


@SolverFactory.register(day=6)
class SolverDay6(PuzzleSolver):
    def __init__(self, input_file: Path):
        super().__init__(input_file=input_file)

    @property
    def demo_result_1(self) -> Optional[int]:
        return 11

    @property
    def demo_result_2(self) -> Optional[int]:
        return 6

    def _read_file(self) -> List[List[Set[str]]]:
        # List of groups
        groups: List[List[Set[str]]] = []
        # List of persons, unique question chars for each person
        cur_group: List[Set[str]] = []
        with open(self._input_file, mode="r") as f:
            for line in f:
                line = line.strip()
                if len(line) == 0:
                    if len(cur_group) > 0:
                        groups.append(cur_group)
                    cur_group = []
                else:
                    cur_group.append(set(line))
            if len(cur_group) > 0:
                groups.append(cur_group)
        return groups

    def solve_1(self) -> int:
        tot_count = 0
        for group in self._input_data:
            uniques = set()
            for person in group:
                uniques.update(person)
            count = len(uniques)
            logger.debug(f"Unique count in current group: {count}")
            tot_count += count
        return tot_count

    def solve_2(self) -> int:
        tot_count = 0
        for group in self._input_data:
            commons = None
            for person in group:
                if commons is None:
                    commons = person
                else:
                    commons = commons.intersection(person)
            count = len(commons)
            logger.debug(f"Common count in current group: {count}")
            tot_count += count
        return tot_count
