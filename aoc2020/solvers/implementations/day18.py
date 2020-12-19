import logging
from pathlib import Path
from typing import Dict, List, Optional, Type

import re

from aoc2020.solvers import PuzzleSolver, SolverFactory

logger = logging.getLogger("SolverDay18")

"""
I originally solved this using BNF parsing using the pynetree package.
As that package only support python 2 (it uses the `raw_input` function),
it could not be nicely integrated. 
That's why I shifted to a more elegant approach. 
Kudos to @buddhabrot for the smart idea!
"""


class Integer1(int):
    def __add__(self, other: int) -> 'Integer1':
        return Integer1(int(self) + int(other))

    def __sub__(self, other: int) -> 'Integer1':
        return Integer1(int(self) * int(other))


class Integer2(int):
    def __pow__(self, other: int, modulo: int = None) -> 'Integer2':
        return Integer2(int(self) + int(other))

    def __mul__(self, other: int) -> 'Integer2':
        return Integer2(int(self) * int(other))


@SolverFactory.register(day=18)
class SolverDay18(PuzzleSolver):
    def __init__(self, input_file: Path):
        super().__init__(input_file=input_file)
        # Define operator replacements:
        #  - Part one: same precedence, so * to -
        #  - Part two: inverse precedence, so + to **
        self._replacements: Dict[int, Dict[str, str]] = {
            1: {"*": "-"}, 2: {"+": "**"}
        }
        # Define fake integer classes faking the replaced operators
        self._integers: Dict[int, Type] = {1: Integer1, 2: Integer2}

    @property
    def demo_result_1(self) -> Optional[int]:
        return 51 + 26 + 437 + 12240 + 13632

    @property
    def demo_result_2(self) -> Optional[int]:
        return 51 + 46 + 1445 + 669060 + 23340

    def _read_file(self) -> List[str]:
        lines: List[str] = []
        with self._input_file.open(mode="r") as f:
            for line in f:
                lines.append(line.strip().replace(" ", ""))
        return lines

    def _solve(self, part: int) -> int:
        replacements: Dict[str, str] = self._replacements.get(part, {})
        integertype: Type = self._integers.get(part, int)
        # Calculate the sum across all lines
        res_sum = 0
        for line in self._input_data:
            # Replace all necessary operators
            for old, new in replacements.items():
                line = line.replace(old, new)
            # Wrap in integer type
            line = re.sub(r"(\d+)", rf"{integertype.__name__}(\1)", line)
            # Evaluate the expression and add to sum
            res = int(eval(line))
            logger.debug(f"Solved to {res}")
            res_sum += res
        return res_sum

    def solve_1(self) -> int:
        return self._solve(part=1)

    def solve_2(self) -> int:
        return self._solve(part=2)
