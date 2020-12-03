import logging
from pathlib import Path
from typing import Dict, Type

from aoc2020.solvers.puzzle_solver import PuzzleSolver

logger = logging.getLogger("SolverFactory")


class SolverFactory:
    registry: Dict[int, Type[PuzzleSolver]] = {}

    @classmethod
    def create_solver(cls, day: int, input_file: Path) -> PuzzleSolver:
        if day not in cls.registry:
            raise ValueError(f"No solver registered for day {day}")

        solver_class = cls.registry[day]
        return solver_class(input_file=input_file)

    @classmethod
    def register(cls, day: int):

        def wrapper(solver_class: Type[PuzzleSolver]) -> Type[PuzzleSolver]:
            if day in cls.registry:
                logger.warning(
                    f"Solver for day {day} already exists. Will overwrite it"
                )
            cls.registry[day] = solver_class
            return solver_class

        return wrapper
