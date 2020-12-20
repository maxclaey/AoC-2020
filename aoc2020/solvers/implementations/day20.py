import logging
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np

from aoc2020.solvers import PuzzleSolver, SolverFactory

logger = logging.getLogger("SolverDay20")


@dataclass
class Augmentation:
    rotation: int = 0
    fliplr: bool = False
    flipud: bool = False


class Direction(Enum):
    TOP = (0, 1)
    BOTTOM = (2, 1)
    LEFT = (1, 0)
    RIGHT = (1, 2)


@SolverFactory.register(day=20)
class SolverDay20(PuzzleSolver):
    def __init__(self, input_file: Path):
        super().__init__(input_file=input_file)
        self.monster = np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1],
            [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0]
        ])

    @property
    def demo_result_1(self) -> Optional[int]:
        return 20899048083289

    @property
    def demo_result_2(self) -> Optional[int]:
        return 273

    def _read_file(self) -> Dict[int, np.ndarray]:
        tiles: Dict[int, np.ndarray] = {}
        conv = {"#": 1, ".": 0}
        with self._input_file.open(mode="r") as f:
            cur_tile_id: int = 0
            cur_lines: List[List[int]] = []
            for line in f:
                line = line.strip()
                if len(line) == 0:
                    if len(cur_lines) > 0:
                        tiles[cur_tile_id] = np.asarray(cur_lines)
                    cur_lines = []
                elif line.startswith("Tile "):
                    cur_tile_id = int(line.split(" ")[1][:-1])
                else:
                    cur_lines.append(list(map(lambda x: conv[x], line)))
        if len(cur_lines) > 0:
            tiles[cur_tile_id] = np.asarray(cur_lines)
        return tiles

    def _find_neighbours(self) -> Dict[int, np.ndarray]:
        tiles = self._input_data
        neighbourmap: Dict[int, np.ndarray] = {}
        for tile_id, target_tile in tiles.items():
            borders = self._get_borders(tile=target_tile)
            # Keep track of the neighbours
            neighbours = np.zeros((3, 3), dtype=np.int)
            # Loop over all other tiles
            for pos_id, pos_tile in tiles.items():
                if pos_id == tile_id:
                    continue
                # Get all borders of the candidate tile
                lines = list(self._get_borders(pos_tile).values())
                # Also consider flipped lines
                alllines = lines + list(map(np.flip, lines))
                for line in alllines:
                    for direction, border in borders.items():
                        if np.array_equal(line, border):
                            assert neighbours[direction.value] == 0
                            neighbours[direction.value] = pos_id
            neighbourmap[tile_id] = neighbours
        return neighbourmap

    @staticmethod
    def _get_borders(
        tile: np.ndarray, augmentation: Augmentation = Augmentation()
    ) -> Dict[Direction, np.ndarray]:
        target_tile = SolverDay20._augment_matrix(
            matrix=tile, augmentation=augmentation
        )
        return {
            Direction.TOP: target_tile[0, :],
            Direction.BOTTOM: target_tile[-1, :],
            Direction.LEFT: target_tile[:, 0],
            Direction.RIGHT: target_tile[:, -1]
        }

    @staticmethod
    def _augment_matrix(
        matrix: np.ndarray, augmentation: Augmentation = Augmentation()
    ) -> np.ndarray:
        target_matrix = np.copy(matrix)
        target_matrix = np.rot90(target_matrix, k=augmentation.rotation)
        if augmentation.fliplr:
            target_matrix = np.fliplr(target_matrix)
        if augmentation.flipud:
            target_matrix = np.flipud(target_matrix)
        return target_matrix

    @staticmethod
    def _find_corners(neighbourmap: Dict[int, np.ndarray]) -> List[int]:
        corners = []
        for tile_id, neighbours in neighbourmap.items():
            num_neigh = np.sum(np.minimum(neighbours, 1))
            if num_neigh == 2:
                corners.append(tile_id)
        return corners

    @staticmethod
    def _find_augmentation(
        tile: np.ndarray, line: np.ndarray, direction: Direction
    ) -> Augmentation:
        for rotation in range(4):
            for fliplr in range(2):
                for flipud in range(2):
                    augmentation = Augmentation(
                        rotation=rotation,
                        fliplr=bool(fliplr),
                        flipud=bool(flipud)
                    )
                    borders = SolverDay20._get_borders(
                        tile=tile, augmentation=augmentation
                    )
                    if np.array_equal(borders[direction], line):
                        return augmentation
        raise ValueError(f"Failed to find augmentation")

    def _reconstruct(self) -> np.ndarray:
        tiles = self._input_data
        # Get the size of the tile matrix
        matrix_size = int(np.sqrt(len(tiles)))
        if not matrix_size**2 == len(tiles):
            raise ValueError(f"Matrix is not square!")

        # Placeholders for reconstruction
        ids = np.zeros((matrix_size, matrix_size), dtype=np.int)
        augmentations: Dict[int, Augmentation] = {}

        # Find the neighbours and corners
        neighbourmap = self._find_neighbours()
        corners = self._find_corners(neighbourmap)

        # Select one of the corners as top-left and define orientation
        top_left_id = corners[0]
        ids[0, 0] = top_left_id
        augmentations[top_left_id] = Augmentation(
            rotation=0,
            fliplr=neighbourmap[top_left_id][Direction.LEFT.value] > 0,
            flipud=neighbourmap[top_left_id][Direction.TOP.value] > 0,
        )

        # Get placeholder for reconstructed image
        tile_size = tiles[top_left_id].shape[0] - 2
        image = np.zeros(
            (matrix_size * tile_size, matrix_size * tile_size), dtype=np.int
        )

        # Iterate over all tiles to find there bottom and right neighbour
        for r in range(matrix_size):
            for c in range(matrix_size):
                tile_id = ids[r, c]
                augmentation = augmentations[tile_id]
                image[
                    r*tile_size:(r+1)*tile_size, c*tile_size:(c+1)*tile_size
                ] = self._augment_matrix(
                    matrix=tiles[tile_id], augmentation=augmentation
                )[1:-1, 1:-1]
                # Get the oriented neighbours
                neighbours = self._augment_matrix(
                    matrix=neighbourmap[tile_id], augmentation=augmentation
                )
                bottom_neighbour = neighbours[2, 1]
                right_neighbour = neighbours[1, 2]
                # Get the bottom and right borders of the current tile
                borders = self._get_borders(
                    tile=tiles[tile_id], augmentation=augmentation
                )
                # Store neighbour information
                if c+1 < matrix_size and ids[r, c+1] == 0:
                    ids[r, c+1] = right_neighbour
                    augmentations[right_neighbour] = self._find_augmentation(
                        tile=tiles[right_neighbour],
                        line=borders[Direction.RIGHT],
                        direction=Direction.LEFT,
                    )

                if r+1 < matrix_size and ids[r+1, c] == 0:
                    ids[r+1, c] = bottom_neighbour
                    augmentations[bottom_neighbour] = self._find_augmentation(
                        tile=tiles[bottom_neighbour],
                        line=borders[Direction.BOTTOM],
                        direction=Direction.TOP,
                    )

        return image

    def _search_monsters(self, image: np.ndarray) -> Tuple[int, int]:
        rows = image.shape[0] - self.monster.shape[0] + 1
        cols = image.shape[1] - self.monster.shape[1] + 1
        subtract = np.zeros_like(image)
        monsters = 0
        # Slide monster over the image
        for r in range(rows):
            for c in range(cols):
                patch = image[
                    r:r+self.monster.shape[0], c:c+self.monster.shape[1]
                ]
                # Count matching monster pixels
                matched = np.sum(
                    np.logical_and(
                        patch.astype(np.bool), self.monster.astype(np.bool)
                    )
                )
                # If monster is matched, keep track which pixels are used
                if matched == np.sum(self.monster):
                    subtract[
                        r:r+self.monster.shape[0], c:c+self.monster.shape[1]
                    ] += self.monster
                    monsters += 1
        # Subtract all monster pixels from the image
        res = image - np.minimum(subtract, 1)
        # Return number of monsters and non monster pixels
        return monsters, int(np.sum(res))

    def solve_1(self) -> int:
        neighbourmap: Dict[int, np.ndarray] = self._find_neighbours()
        corners = self._find_corners(neighbourmap)
        if len(corners) != 4:
            logger.error(f"No solution found!")
            return 0
        return int(np.prod(corners))

    def solve_2(self) -> int:
        image = self._reconstruct()
        for rotation in range(4):
            for fliplr in range(2):
                for flipud in range(2):
                    img = self._augment_matrix(
                        matrix=image,
                        augmentation=Augmentation(
                            rotation=rotation,
                            fliplr=bool(fliplr),
                            flipud=bool(flipud)
                        )
                    )
                    num_monsters, remaining_pixels = self._search_monsters(img)
                    if num_monsters > 0:
                        return remaining_pixels
        logger.error(f"Could not find a solution for task 2")
        return 0
