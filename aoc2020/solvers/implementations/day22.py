import logging
import sys
from collections import defaultdict, deque
from pathlib import Path
from typing import Deque, Dict, List, Optional, Set, Tuple

from aoc2020.solvers import PuzzleSolver, SolverFactory

logger = logging.getLogger("SolverDay22")
# Increase recursion limit
sys.setrecursionlimit(10**6)


@SolverFactory.register(day=22)
class SolverDay22(PuzzleSolver):
    def __init__(self, input_file: Path):
        super().__init__(input_file=input_file)

    @property
    def demo_result_1(self) -> Optional[int]:
        return 306

    @property
    def demo_result_2(self) -> Optional[int]:
        return 291

    def _read_file(self) -> Dict[int, List[int]]:
        player_id = -1
        decks: Dict[int, List[int]] = defaultdict(list)
        with open(self._input_file, mode="r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("Player"):
                    try:
                        player_id = int(line[:-1].split(" ")[1])
                    except ValueError:
                        logger.error(f"Failed to parse player line")
                elif len(line) > 0:
                    assert player_id > 0
                    try:
                        card = int(line)
                        decks[player_id].append(card)
                    except ValueError:
                        logger.error(f"Failed to parse card line")
        return decks

    @staticmethod
    def _play_normal(
        deck1: Deque[int], deck2: Deque[int]
    ) -> Tuple[int, Deque[int]]:
        if len(deck1) == 0:
            return 1, deck2
        elif len(deck2) == 0:
            return 2, deck1
        card1 = deck1.popleft()
        card2 = deck2.popleft()
        if card1 > card2:
            deck1.append(card1)
            deck1.append(card2)
        else:
            deck2.append(card2)
            deck2.append(card1)
        return SolverDay22._play_normal(deck1, deck2)

    @staticmethod
    def _play_recursive(
        deck1: Deque[int],
        deck2: Deque[int],
        history: Optional[Set[int]] = None,
    ) -> Tuple[int, Deque[int]]:
        if history is None:
            history = set()
        # Key for state: hash of two decks
        key = hash((tuple(deck1), tuple(deck2)))
        # Player 1 wins if in state seen before or when player 2 has no cards
        winner = 1 if len(deck2) == 0 or key in history else 0
        # Player 2 wins if player 1 has no cards
        winner = 2 if len(deck1) == 0 else winner
        if winner > 0:
            return winner, deck1 if winner == 1 else deck2
        # No winner, play round
        history.add(key)
        card1 = deck1.popleft()
        card2 = deck2.popleft()
        # When both players have enough cards for recursion, recurse
        if card1 <= len(deck1) and card2 <= len(deck2):
            recurse_deck1 = deque(list(deck1)[:card1])
            recurse_deck2 = deque(list(deck2)[:card2])
            winner, _ = SolverDay22._play_recursive(
                deck1=recurse_deck1, deck2=recurse_deck2, history=set()
            )
        # When someone has not enough cards, player with highest card wins
        else:
            winner = 1 if card1 > card2 else 2
        # Add cards to winners deck and recurse
        winner_deck = deck1 if winner == 1 else deck2
        winner_deck.append(card1 if winner == 1 else card2)
        winner_deck.append(card2 if winner == 1 else card1)
        return SolverDay22._play_recursive(
            deck1=deck1, deck2=deck2, history=history,
        )

    @staticmethod
    def _score_deck(deck: Deque[int]) -> int:
        score = 0
        for i, val in enumerate(reversed(deck)):
            score += (i+1)*val
        return score

    def solve_1(self) -> int:
        decks = self._input_data
        deck1 = deque(decks[1])
        deck2 = deque(decks[2])
        _, winner_deck = self._play_normal(deck1, deck2)
        return self._score_deck(winner_deck)

    def solve_2(self) -> int:
        decks = self._input_data
        deck1 = deque(decks[1])
        deck2 = deque(decks[2])
        _, winner_deck = self._play_recursive(deck1, deck2, set())
        return self._score_deck(winner_deck)
