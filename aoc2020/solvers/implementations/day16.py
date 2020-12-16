import logging
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

from aoc2020.solvers import PuzzleSolver, SolverFactory

logger = logging.getLogger("SolverDay16")

TicketFields = Dict[str, List[Tuple[int, int]]]
Ticket = List[int]


@SolverFactory.register(day=16)
class SolverDay16(PuzzleSolver):
    def __init__(self, input_file: Path):
        super().__init__(input_file=input_file)

    @property
    def demo_result_1(self) -> Optional[int]:
        return 71

    @property
    def demo_result_2(self) -> Optional[int]:
        return None

    def _read_file(self) -> Tuple[TicketFields, Ticket, List[Ticket]]:
        stage = 0
        fields: TicketFields = {}
        my_ticket: Ticket = []
        nearby_tickets: List[Ticket] = []
        with self._input_file.open(mode="r") as f:
            for line in f:
                line = line.strip()
                if line == "your ticket:":
                    stage = 1
                elif line == "nearby tickets:":
                    stage = 2
                elif stage == 0:
                    field = self._parse_field(line=line)
                    if field is not None:
                        name, ranges = field
                        fields[name] = ranges
                else:
                    try:
                        values = list(
                            map(lambda x: int(x.strip()), line.split(","))
                        )
                    except ValueError:
                        logger.error(f"Invalid ticket: {line}")
                        continue
                    if stage == 1:
                        if len(my_ticket) != 0:
                            logger.error(f"Found duplicate of my ticket!")
                            continue
                        my_ticket = values
                    else:
                        if len(values) != len(my_ticket):
                            logger.error(f"Found tickets of different length")
                            continue
                        nearby_tickets.append(values)
        return fields, my_ticket, nearby_tickets

    @staticmethod
    def _parse_field(line: str) -> Optional[Tuple[str, List[Tuple[int, int]]]]:
        parts = line.split(":")
        if len(parts) != 2:
            logger.error(f"Invalid field line: {line}")
            return None
        name: str = parts[0].strip()
        ranges = parts[1].split(" or ")
        num_ranges: List[Tuple[int, int]] = []
        for r in ranges:
            try:
                numbers = list(map(lambda x: int(x.strip()), r.split("-")))
            except ValueError:
                logger.error(f"Invalid number range {r}")
                return None
            if len(numbers) != 2:
                logger.error(f"Invalid number range {r}")
                return None
            num_ranges.append((numbers[0], numbers[1]))
        return name, num_ranges

    @staticmethod
    def _valid_fields(
        fields: TicketFields, ticket: Ticket
    ) -> Tuple[Optional[int], Dict[str, Set[int]]]:
        # For each field, keep track of the value indices that satisfy this field
        possible_indices: Dict[str, Set[int]] = {f: set() for f in fields}
        # Iterate over ticket fields
        for i, val in enumerate(ticket):
            val_ok = False
            for field, ranges in fields.items():
                # Check if value matches one of the ranges for this field
                for r in ranges:
                    if r[0] <= val <= r[1]:
                        possible_indices[field].add(i)
                        val_ok = True
                        continue
            # Value could not be matched to any ticket, so invalid ticket
            if not val_ok:
                return val, {}
        return None, possible_indices

    @staticmethod
    def _extract_mapping(
        possible_indices: Dict[str, Set[int]], mapping: Dict[str, int]
    ) -> Dict[str, int]:
        # No more fields to still match
        if len(possible_indices) == 0:
            return mapping
        # Sort the fields on least possible indices
        sorted_map = sorted(possible_indices.items(), key=lambda x: len(x[1]))
        field, pos = sorted_map[0]
        # There should at least be one field that only has 1 possible index
        #  to be deterministic
        if len(pos) != 1:
            raise ValueError(f"Cannot find deterministic field mapping")
        index = list(pos)[0]
        # Add field-index mapping
        mapping[field] = index
        del possible_indices[field]
        # As this index is mapped, remove it from all other possible fields
        for field in possible_indices:
            if index in possible_indices[field]:
                possible_indices[field].remove(index)
        # Recurse until solution is found
        return SolverDay16._extract_mapping(possible_indices, mapping)

    def solve_1(self) -> int:
        fields, _, nearby_tickets = self._input_data
        # Keep track of all invalid values
        invalid_vals = []
        for ticket in nearby_tickets:
            invalid_val, _ = self._valid_fields(fields, ticket)
            if invalid_val is not None:
                invalid_vals.append(invalid_val)
        return sum(invalid_vals)

    def solve_2(self) -> int:
        fields, my_ticket, nearby_tickets = self._input_data
        # Consider own ticket as well
        all_tickets = nearby_tickets + [my_ticket]
        # To start, each field could be any ticket index
        pos_indices = {f: set(range(len(my_ticket))) for f in fields}
        # Validate each ticket
        for ticket in all_tickets:
            invalid_val, ticket_ids = self._valid_fields(fields, ticket)
            # Skip invalid tickets
            if invalid_val is not None:
                continue
            # Keep track of new possible field-index assignments
            for f in pos_indices:
                pos_indices[f] = pos_indices[f].intersection(ticket_ids[f])
        # Extract the mapping from the possible indices
        mapping = self._extract_mapping(pos_indices, {})
        mul = 1
        # Multiply all values in my ticket for fields that start with departure
        for field, index in mapping.items():
            if field.startswith("departure"):
                mul *= my_ticket[index]
        return mul
