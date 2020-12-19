import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import re

from aoc2020.solvers import PuzzleSolver, SolverFactory

logger = logging.getLogger("SolverDay19")


@SolverFactory.register(day=19)
class SolverDay19(PuzzleSolver):
    def __init__(self, input_file: Path):
        super().__init__(input_file=input_file)

    @property
    def demo_result_1(self) -> Optional[int]:
        return 3

    @property
    def demo_result_2(self) -> Optional[int]:
        return 12

    def _read_file(self) -> Tuple[Dict[int, str], List[str]]:
        rules: Dict[int, str] = {}
        messages: List[str] = []
        with self._input_file.open(mode="r") as f:
            for line in f:
                parts = line.strip().split(":")
                # 2 parts -> line is a rule
                if len(parts) == 2:
                    try:
                        rules[int(parts[0])] = parts[1].strip()
                    except ValueError:
                        logger.error(f"Failed to parse rule ID {parts[0]}")
                # 1 part, non empty -> message
                elif len(parts) == 1 and len(parts[0]) > 0:
                    messages.append(parts[0])
        return rules, messages

    def _parse_rule(
        self,
        rule_id: int,
        processed_rules: Optional[Dict[int, str]] = None,
        part_two: bool = False,
    ) -> str:
        if processed_rules is None:
            processed_rules = {}
        # If rule already processed, return immediately
        if rule_id in processed_rules:
            return processed_rules[rule_id]
        rules, _ = self._input_data
        rule = rules[rule_id]
        if re.match('^"[a-z]+"$', rule):
            processed_rules[rule_id] = rule[1:-1]
            return processed_rules[rule_id]
        else:
            options = rule.split(" | ")
            subrules = []
            # Loop over all options
            for option in options:
                # Get the sub rule IDs for this option
                sub_ids = option.split(" ")
                parts = []
                # Parse all parts recursively
                for sub_id in sub_ids:
                    parts.append(
                        self._parse_rule(
                            rule_id=int(sub_id),
                            processed_rules=processed_rules,
                            part_two=part_two,
                        )
                    )
                # In part two, update rule eleven into multiple rules
                if part_two and rule_id == 11:
                    assert len(parts) == 2
                    for n in range(1, 6):
                        subrules.append(f'{parts[0]}{{{n}}}{parts[1]}{{{n}}}')
                # Normal mode: concatenate strings
                else:
                    subrules.append("".join(parts))
            # Only 1 subrule -> take as rule
            if len(subrules) == 1:
                combined = subrules[0]
            # Multiple subrules -> or them
            else:
                combined = f"({'|'.join(subrules)})"
            # In part two, update rule eight
            if part_two and rule_id == 8:
                combined = f"{combined}+"
            # Store processed rule and return
            processed_rules[rule_id] = combined
            return combined

    def solve_1(self) -> int:
        _, messages = self._input_data
        regex = self._parse_rule(rule_id=0)
        valids = 0
        for message in messages:
            if re.fullmatch(regex, message) is not None:
                valids += 1
        return valids

    def solve_2(self) -> int:
        _, messages = self._input_data
        regex = self._parse_rule(rule_id=0, part_two=True)
        valids = 0
        for message in messages:
            if re.fullmatch(regex, message) is not None:
                valids += 1
        return valids
