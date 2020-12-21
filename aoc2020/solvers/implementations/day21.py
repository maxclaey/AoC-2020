import logging
from collections import Counter
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

import re

from aoc2020.solvers import PuzzleSolver, SolverFactory

logger = logging.getLogger("SolverDay21")


@SolverFactory.register(day=21)
class SolverDay21(PuzzleSolver):
    def __init__(self, input_file: Path):
        super().__init__(input_file=input_file)

    @property
    def demo_result_1(self) -> Optional[int]:
        return 5

    @property
    def demo_result_2(self) -> Optional[str]:
        return "mxmxvkd,sqjhc,fvjkl"

    def _read_file(self) -> List[Tuple[List[str], List[str]]]:
        foods: List[Tuple[List[str], List[str]]] = []
        pattern = r"([^\(]*) \(contains (.*)\)"
        with open(self._input_file, mode="r") as f:
            for line in f:
                m = re.fullmatch(pattern, line.strip())
                if m:
                    ingredients = m.group(1).split(" ")
                    allergens = m.group(2).split(", ")
                    foods.append((ingredients, allergens))
                else:
                    logger.error(f'Failed to parse line {line}')
        return foods

    def _map_allergens_to_ingredients(self) -> Dict[str, Set[str]]:
        foods = self._input_data
        # Mapping between allergens and ingredients possibly containing it
        mapping: Dict[str, Set[str]] = {}
        # Iterate all foods
        for ingredients, allergens in foods:
            for allergen in allergens:
                if allergen not in mapping:
                    mapping[allergen] = set(ingredients)
                else:
                    mapping[allergen] = mapping[allergen].intersection(
                        ingredients
                    )
        return mapping

    def _solve_mapping(
        self,
        mapping: Dict[str, Set[str]], solution: Dict[str, str]
    ) -> Dict[str, str]:
        # When there are no more possible mappings, solution is found
        if len(mapping) == 0:
            return solution
        # Sort allergens from least to most possible ingredients
        sorted_mapping = list(sorted(mapping.items(), key=lambda x: len(x[1])))
        # Select the first allergen, it should only have one possible
        #  ingredient to be solvable
        allergen, ingredients = sorted_mapping[0]
        if len(ingredients) > 1:
            logger.error(
                f"Expected at least one allergen with only one possible "
                f"ingredient. This mapping cannot be solved."
            )
            return {}
        ingredient = list(ingredients)[0]
        solution[allergen] = ingredient
        # Delete allergen from mapping as it's now part of the solution
        del mapping[allergen]
        # Remove matched ingredient from all other possible mappings
        for allergen, ingredients in mapping.items():
            if ingredient in ingredients:
                ingredients.remove(ingredient)
        # Solve recursively
        return self._solve_mapping(mapping, solution)

    def solve_1(self) -> int:
        foods = self._input_data
        mapping = self._map_allergens_to_ingredients()

        # Get all ingredients (as set)
        all_ingredients: List[str] = sum([list(i) for i, _ in foods], [])
        ingredients_set: Set[str] = set(all_ingredients)

        # Count occurrences of all ingredients
        ingredients_count: Dict[str, int] = Counter(all_ingredients)

        # Get all ingredients that possibly have allergens
        possible_allergens: Set[str] = set(sum(
            [list(i) for i in mapping.values()], []
        ))

        # Get all ingredients that don't have allergens
        no_allergens = ingredients_set - possible_allergens

        # Count the number of times these ingredients occur
        return sum([ingredients_count.get(i, 0) for i in no_allergens])

    def solve_2(self) -> str:
        mapping = self._map_allergens_to_ingredients()
        # Solve the mapping to find which allergen is found in which ingredient
        solution = self._solve_mapping(mapping=mapping, solution={})
        # Join values with comma, based on sorted keys
        key = ",".join(ingr for _, ingr in sorted(solution.items()))
        return key
