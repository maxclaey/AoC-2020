import logging
from pathlib import Path
from typing import List, Optional, Tuple

from aoc2020.solvers import PuzzleSolver, SolverFactory

logger = logging.getLogger("SolverDay8")


@SolverFactory.register(day=8)
class SolverDay8(PuzzleSolver):
    def __init__(self, input_file: Path):
        super().__init__(input_file=input_file)
        self._accumulator: int = 0

    @property
    def demo_result_1(self) -> Optional[int]:
        return 5

    @property
    def demo_result_2(self) -> Optional[int]:
        return 8

    def _read_file(self) -> List[Tuple[str, int]]:
        instructions: List[Tuple[str, int]] = []
        for line in self._input_file.open(mode="r"):
            parts = line.split(" ")
            if len(parts) != 2:
                logger.error(f"Could not parse line {line}")
                continue
            instruction = parts[0].strip()
            try:
                step = int(parts[1].strip())
            except ValueError:
                logger.error(f"Invalid instruction {line}")
                continue
            instructions.append((instruction, step))
        return instructions

    def _handle_instruction(self, index: int) -> int:
        assert index < len(self._input_data)
        instruction, step = self._input_data[index]
        if instruction == "nop":
            return index + 1
        elif instruction == "acc":
            self._accumulator += step
            return index + 1
        elif instruction == "jmp":
            return index + step
        else:
            raise ValueError(f"Invalid instruction {instruction}")

    def _run_program(self) -> bool:
        visited_indices = set()
        self._accumulator = 0
        index = 0
        while True:
            if index >= len(self._input_data):
                break
            elif index in visited_indices:
                logger.debug(f"Loop detected, value is {self._accumulator}")
                return False
            else:
                visited_indices.add(index)
                index = self._handle_instruction(index=index)
        return True

    def solve_1(self) -> int:
        finished = self._run_program()
        if not finished:
            logger.debug(f"Loop detected, value is {self._accumulator}")
            return self._accumulator
        else:
            logger.error(f"No solution found")
            return 0

    def solve_2(self) -> int:
        for i in range(len(self._input_data)):
            instr, step = self._input_data[i]
            if instr == "jmp":
                new_instr = "nop"
            elif instr == "nop":
                new_instr = "jmp"
            else:
                continue
            self._input_data[i] = (new_instr, step)
            finished = self._run_program()
            self._input_data[i] = (instr, step)
            if finished:
                logger.debug(
                    f"Found a combination that terminates the program: "
                    f"flipping instruction {i} from '{instr} {step}' to "
                    f"'{new_instr} {step}'"
                )
                return self._accumulator
        logger.error(f"No solution found")
        return 0
