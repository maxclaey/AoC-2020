import logging
from pathlib import Path
from typing import Optional, Tuple

from aoc2020.solvers import PuzzleSolver, SolverFactory

logger = logging.getLogger("SolverDay25")


@SolverFactory.register(day=25)
class SolverDay25(PuzzleSolver):
    def __init__(self, input_file: Path):
        super().__init__(input_file=input_file)
        self._divisor: int = 20201227

    @property
    def demo_result_1(self) -> Optional[int]:
        return 14897079

    @property
    def demo_result_2(self) -> Optional[int]:
        return 0

    def _read_file(self) -> Tuple[int, int]:
        with open(self._input_file, mode="r") as f:
            try:
                lines = [int(line.strip()) for line in f]
                if len(lines) == 2:
                    return lines[0], lines[1]
                else:
                    logger.error(f"Expected 2 values, got {len(lines)}")
            except ValueError:
                logger.error(f"Failed to decode the input file")
        return 0, 0

    def _transform(self, subject_nr: int, loop_size: int) -> int:
        value: int = 1
        for _ in range(loop_size):
            value = (value * subject_nr) % self._divisor
        return value

    def _get_loopsize(self, key: int, subject_nr: int) -> int:
        value = 1
        loop_size = 0
        while True:
            loop_size += 1
            value = (value * subject_nr) % self._divisor
            if value == key:
                return loop_size

    def solve_1(self) -> int:
        subject_nr = 7
        card_key, door_key = self._input_data
        card_loop = self._get_loopsize(key=card_key, subject_nr=subject_nr)
        logger.debug(f"Card loop size is {card_loop}")
        enc_key = self._transform(subject_nr=door_key, loop_size=card_loop)
        return enc_key

    def solve_2(self) -> int:
        logger.info(f"There's no part 2 on day 25..")
        return 0
