import logging
from pathlib import Path
from typing import Dict, List, Optional

from aoc2020.solvers import PuzzleSolver, SolverFactory

logger = logging.getLogger("SolverDay23")


class Node:
    def __init__(
        self,
        value: int,
        nxt: "Node" = None,
    ):
        self.value: int = value
        self.next: "Node" = nxt  # type: ignore

    def __str__(self):
        return f"{self.value:d}"


class LinkedList:
    def __init__(self, values: List[int]):
        self.head: Node = Node(values[-1])
        last = self.head
        # Mapping from value to node, for quick lookup
        self.nodemap: Dict[int, Node] = {values[-1]: self.head}
        self.minimum: int = min(values)
        self.maximum: int = max(values)
        for val in reversed(values[:-1]):
            self.head = Node(val, nxt=self.head)
            self.nodemap[val] = self.head
        last.next = self.head

    def remove(self, node: Node):
        if node == self.head:
            self.head = self.head.next
        pointer = self.head
        while pointer.next != node:
            pointer = pointer.next
        pointer.next = node.next

    @staticmethod
    def get_values_after(node: Node, count: int) -> List[int]:
        values: List[int] = []
        for i in range(count):
            values.append(node.next.value)
            node = node.next
        return values

    @staticmethod
    def move_tail(src: Node, dst: Node, count: int) -> None:
        first = src.next
        last = first
        for i in range(count-1):
            last = last.next
        src.next = last.next
        last.next = dst.next
        dst.next = first

    def move_head(self, node: Node) -> None:
        self.head = node

    def search(self, value: int) -> Node:
        return self.nodemap[value]

    def __str__(self):
        output = f"{self.head.value}"
        node = self.head.next
        while node != self.head:
            output += f"{node.value}"
            node = node.next
        return output


@SolverFactory.register(day=23)
class SolverDay23(PuzzleSolver):
    def __init__(self, input_file: Path):
        super().__init__(input_file=input_file)

    @property
    def demo_result_1(self) -> Optional[str]:
        return "67384529"

    @property
    def demo_result_2(self) -> Optional[int]:
        return 149245887792

    def _read_file(self) -> List[int]:
        cups: List[int] = []
        with open(self._input_file, mode="r") as f:
            for line in f:
                line = line.strip()
                cups = list(map(int, line))
        return cups

    @staticmethod
    def _play_game(cups: LinkedList, rounds: int) -> LinkedList:
        cup: Node = cups.head
        for _ in range(rounds):
            # Pick 3 cups after the current cup
            picked_values: List[int] = cups.get_values_after(node=cup, count=3)
            # Find the cup where we want to move the cups after
            index: int = cup.value - 1
            while index in picked_values or index < cups.minimum:
                index = index - 1 if index > cups.minimum else cups.maximum
            # Find the node with the given index in the list
            target: Node = cups.search(index)
            # Move the 3 cups from after the current cup to after the target
            cups.move_tail(cup, target, 3)
            # Move the head one forward
            cup = cup.next
        return cups

    def solve_1(self) -> str:
        cups = LinkedList(self._input_data)
        cups = self._play_game(cups, 100)
        # Find the cup with index 1
        one = cups.search(1)
        # Move head to right after 1 and remove one
        cups.move_head(one.next)
        cups.remove(one)
        # Return string representation of the list
        return str(cups)

    def solve_2(self) -> int:
        starter = self._input_data
        intcups = starter + list(range(max(starter)+1, int(1e6+1)))
        cups = LinkedList(intcups)
        cups = self._play_game(cups, int(1e7))
        # Find the cup with index 1
        one = cups.search(1)
        # Get the 2 values after the one
        val1 = one.next
        val2 = val1.next
        logger.debug(f"Needed values are {val1.value} and {val2.value}")
        return val1.value * val2.value
