import logging
from pathlib import Path
from typing import List, Optional, Tuple, Union

from aoc2020.solvers import PuzzleSolver, SolverFactory

logger = logging.getLogger("SolverDay14")


@SolverFactory.register(day=14)
class SolverDay14(PuzzleSolver):
    def __init__(self, input_file: Path):
        super().__init__(input_file=input_file)

    @property
    def demo_result_1(self) -> Optional[int]:
        return 51

    @property
    def demo_result_2(self) -> Optional[int]:
        return 208

    def _read_file(self) -> List[Union[str, Tuple[int, int]]]:
        instructions: List[Union[str, Tuple[int, int]]] = []
        with self._input_file.open(mode="r") as f:
            for line in f:
                parts = line.strip().split(" = ")
                if len(parts) != 2:
                    logger.error(f"Could not parse line {line}")
                    continue
                if parts[0] == "mask":
                    if len(parts[1]) != 36:
                        logger.error(f"Invalid mask {parts[1]}")
                        continue
                    instructions.append(parts[1])
                elif parts[0].startswith("mem["):
                    try:
                        index = int(parts[0][4:-1])
                        instructions.append((index, int(parts[1])))
                    except ValueError:
                        logger.error(f"Invalid memory assigment {line}")
                        continue
                else:
                    logger.error(f"Invalid instruction {parts[0]}")
                    continue
        return instructions

    @staticmethod
    def _mask(value: int, mask: str) -> int:
        bitstring = list(f"{value:036b}")
        for i, c in enumerate(mask):
            if c != "X":
                bitstring[i] = c
        return int("".join(bitstring), 2)

    @staticmethod
    def _mask_floating(value: int, mask: str) -> List[int]:
        results = [list(f"{value:036b}")]
        for i, c in enumerate(mask):
            if c == "1":
                for res in results:
                    res[i] = "1"
            elif c == "X":
                new_results = []
                for res in results:
                    newres0 = res.copy()
                    newres0[i] = "0"
                    new_results.append(newres0)
                    newres1 = res.copy()
                    newres1[i] = "1"
                    new_results.append(newres1)
                results = new_results
        return [int("".join(bs), 2) for bs in results]

    def solve_1(self) -> int:
        mask = "X" * 36
        memory = {}
        for instr in self._input_data:
            if isinstance(instr, str):
                mask = instr
            else:
                index, value = instr
                memory[index] = self._mask(value=value, mask=mask)
        return sum(memory.values())

    def solve_2(self) -> int:
        mask = "X" * 36
        memory = {}
        for instr in self._input_data:
            if isinstance(instr, str):
                mask = instr
            else:
                index, value = instr
                indices = self._mask_floating(value=index, mask=mask)
                for index in indices:
                    memory[index] = value
        return sum(memory.values())
