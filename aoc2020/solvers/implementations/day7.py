import logging
import re
from pathlib import Path
from typing import Dict, Optional, Tuple

from aoc2020.solvers import PuzzleSolver, SolverFactory

logger = logging.getLogger("SolverDay7")


@SolverFactory.register(day=7)
class SolverDay7(PuzzleSolver):
    def __init__(self, input_file: Path):
        super().__init__(input_file=input_file)

    @property
    def demo_result_1(self) -> Optional[int]:
        return 4

    @property
    def demo_result_2(self) -> Optional[int]:
        return 32

    def _read_file(self) -> Dict[str, Dict[str, int]]:
        # Mapping bags to containing bags and counts
        rules: Dict[str, Dict[str, int]] = {}
        for line in self._input_file.open(mode="r"):
            res = self._parse_line(line)
            if res is not None:
                bag_type, content = res
                rules[bag_type] = content
        return rules

    @staticmethod
    def _parse_line(line: str) -> Optional[Tuple[str, Dict[str, int]]]:
        line = line.strip().replace(".", "").replace(" no ", " 0 ")
        # Main string pattern
        pattern = "^(.*) bags contain (([0-9]+) (.*) bag[s]?[,]?)+$"
        # Content part pattern
        content_pattern = "^([0-9]+) (.*) bag[s]?$"
        content: Dict[str, int] = {}
        # Main matching
        match = re.fullmatch(pattern, line)
        if match is None:
            logger.error(f"Failed to match line {line}")
            return None
        bag_type = match.group(1)
        content_str = match.group(2)
        for part in content_str.split(","):
            part = part.strip()
            submatch = re.fullmatch(content_pattern, part)
            if submatch is None:
                logger.error(f"Failed to parse content part {part}")
                return None
            count = int(submatch.group(1).strip())
            sub_type = submatch.group(2).strip()
            content[sub_type] = count
        return bag_type, content

    def _can_contain(self, bag: str, content: str) -> bool:
        bag_rules = self._input_data.get(bag, {})
        for part, count in bag_rules.items():
            # Don't consider empty bags
            if count == 0:
                continue
            # If it directly contains is, great
            if part == content:
                return True
            # If it does not directly contain is, check contents
            elif self._can_contain(bag=part, content=content):
                return True
        return False

    def _count_content(self, bag: str) -> int:
        total_count = 0
        bag_rules = self._input_data.get(bag, {})
        for part, count in bag_rules.items():
            if count > 0:
                total_count += count + count * self._count_content(bag=part)
        return total_count

    def solve_1(self) -> int:
        content = "shiny gold"
        count = 0
        for bag_type in self._input_data:
            if self._can_contain(bag=bag_type, content=content):
                count += 1
                logger.debug(f"Bag type {bag_type} can contain a {content}")
        return count

    def solve_2(self) -> int:
        bag = "shiny gold"
        return self._count_content(bag=bag)
