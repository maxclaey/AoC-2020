import logging
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from aoc2020.solvers import PuzzleSolver, SolverFactory

logger = logging.getLogger("SolverDay10")


@SolverFactory.register(day=10)
class SolverDay10(PuzzleSolver):
    def __init__(self, input_file: Path):
        super().__init__(input_file=input_file)
        self.allowed_diffs: List[int] = [1, 2, 3]
        self.internal_diff: int = 3

    @property
    def demo_result_1(self) -> Optional[int]:
        return 220

    @property
    def demo_result_2(self) -> Optional[int]:
        return 19208

    def _read_file(self) -> List[int]:
        values: List[int] = []
        with self._input_file.open(mode="r") as f:
            for line in f:
                try:
                    values.append(int(line.strip()))
                except ValueError:
                    logger.error(f"Invalid line {line}: not an integer")
        return sorted(values)

    def solve_1(self) -> int:
        cur_jolt = 0
        differences = defaultdict(int)
        for adapter in self._input_data:
            diff = adapter - cur_jolt
            if diff not in self.allowed_diffs:
                logger.warning(f"Cannot plug adapter anaymore")
                break
            differences[diff] += 1
            cur_jolt = adapter
        # Internal adapter
        differences[self.internal_diff] += 1
        logger.debug(f"Differences are {differences}")
        return differences[1] * differences[3]

    def _count_possibilities(
        self,
        cur_jolts: int,
        adapters: List[int],
        results_cache: Dict[Tuple[int, int, int], int],
    ) -> int:
        # No more adapters left -> solution found
        if len(adapters) == 0:
            return 1
        # Check results cache: current jolts level, smallest adapter and
        # number of adapters is a unique key for a state
        cache_key = (cur_jolts, adapters[0], len(adapters))
        if cache_key in results_cache:
            return results_cache[cache_key]
        # Count possibilities recursively
        possibilities = 0
        for i, adapter in enumerate(adapters):
            diff = adapter - cur_jolts
            if diff in self.allowed_diffs:
                possibilities += self._count_possibilities(
                    cur_jolts=adapter,
                    adapters=adapters[i+1:],
                    results_cache=results_cache,
                )
            else:
                # In practice we could break here, but not doing it in
                # case allowed_diffs would have gaps
                pass

        results_cache[cache_key] = possibilities
        return possibilities

    def solve_2(self) -> int:
        # Include internal adapter
        all_adapters = self._input_data + [self._input_data[-1]+self.internal_diff]
        return self._count_possibilities(
            cur_jolts=0,
            adapters=all_adapters,
            results_cache={},
        )
