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

    def _read_file(self) -> Tuple[int, List[int]]:
        timestamp: int = 0
        bus_ids: List[int] = []
        with self._input_file.open(mode="r") as f:
            lines = [line.strip() for line in f]
            if len(lines) != 2:
                logger.error(f"Input file contains invalid number of lines")
            else:
                timestamp = int(lines[0])
                busses = lines[1].split(',')
                for bus in busses:
                    try:
                        bus_id = int(bus)
                    except ValueError:
                        bus_id = -1
                    bus_ids.append(bus_id)
        return timestamp, bus_ids

    def solve_1(self) -> int:
        ts, bus_ids = self._input_data
        min_waiting_time: int = -1
        earliest_bus_id: int = 0
        for bus_id in bus_ids:
            if bus_id < 0:
                continue
            # Calculate the waiting time
            waiting_time = int(np.ceil(ts / bus_id)) * bus_id - ts
            # Keep track of lowest waiting time and earliest bus
            if min_waiting_time < 0 or waiting_time < min_waiting_time:
                min_waiting_time = waiting_time
                earliest_bus_id = bus_id
        return min_waiting_time * earliest_bus_id

    def solve_2(self) -> int:
        _, bus_ids = self._input_data
        solution = 0
        freq = 1
        # For each bus, find the earliest time that fits the solution and
        #  the frequency with which the solution will reoccur
        for idx, bus_id in enumerate(bus_ids):
            if bus_id < 0:
                continue
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
