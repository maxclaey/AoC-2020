import logging
from itertools import count
from pathlib import Path
from typing import List, Optional, Tuple

import numpy as np

from aoc2020.solvers import PuzzleSolver, SolverFactory

logger = logging.getLogger("SolverDay13")


@SolverFactory.register(day=13)
class SolverDay13(PuzzleSolver):
    def __init__(self, input_file: Path):
        super().__init__(input_file=input_file)

    @property
    def demo_result_1(self) -> Optional[int]:
        return 295

    @property
    def demo_result_2(self) -> Optional[int]:
        return 1068781

    def _read_file(self) -> Tuple[int, List[str]]:
        timestamp: int = 0
        busses: List[str] = []
        with self._input_file.open(mode="r") as f:
            lines = [line.strip() for line in f]
            if len(lines) != 2:
                logger.error(f"Input file contains invalid number of lines")
            else:
                timestamp = int(lines[0])
                busses = lines[1].split(',')
        return timestamp, busses

    def solve_1(self) -> int:
        timestamp, busses = self._input_data
        arrival_times: List[Tuple[int, int]] = []
        for bus in busses:
            try:
                bus_id = int(bus)
            except ValueError:
                logger.debug(f"Non-numeric bus ID ignored")
                continue
            waiting_time = np.ceil(timestamp / bus_id) * bus_id - timestamp
            arrival_times.append((bus_id, waiting_time))
        arrival_times = list(sorted(arrival_times, key=lambda x: x[1]))
        if len(arrival_times) > 0:
            winner = arrival_times[0]
            return winner[0] * winner[1]
        else:
            logger.error(f"No solution found")
            return 0

    def solve_2(self) -> int:
        constraints: List[Tuple[int, int]] = []
        _, busses = self._input_data
        # Extract the bus IDs and the time constraints
        for idx, bus in enumerate(busses):
            try:
                bus_id = int(bus)
            except ValueError:
                logger.debug(f"Non-numeric bus ID ignored")
                continue
            constraints.append((bus_id, idx))
        solution = 0
        freq = 1
        # For each bus, find the earliest time that fits the solution and
        #  the frequency with which the solution will reoccur
        for bus_id, idx in constraints:
            # Count instead of range for infinite loop
            for timestamp in count(solution, freq):
                # When current ts is a solution for this bus, break and store
                if (timestamp + idx) % bus_id == 0:
                    solution = timestamp
                    break
            # The frequency at which this solution occurs is the least common
            #  multiple of the frequency of the previous solution and the
            #  bus frequency
            freq = np.lcm(freq, bus_id)
        return solution
