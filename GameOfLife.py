from __future__ import annotations

from typing import Iterable, Iterator, Optional, Set, Tuple
from PIL import Image

Coord = Tuple[int, int]


class GameOfLife:
    """
    Conway's Game of Life using a sparse representation.

    Rules:
      - ONLY pixels that are exactly (255,255,255) are alive
      - EVERYTHING else is dead
    """

    def __init__(self, alive: Optional[Iterable[Coord]] = None):
        self.alive: Set[Coord] = set(alive) if alive else set()

    # ----------------------------
    # Neighbour logic
    # ----------------------------
    @staticmethod
    def neighbors(x: int, y: int) -> Iterator[Coord]:
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                yield (x + dx, y + dy)

    # ----------------------------
    # Life step
    # ----------------------------
    def step(self) -> None:
        neighbor_counts: dict[Coord, int] = {}

        # Count neighbours around alive cells ONLY
        for (x, y) in self.alive:
            for n in self.neighbors(x, y):
                neighbor_counts[n] = neighbor_counts.get(n, 0) + 1

        new_alive: Set[Coord] = set()

        for cell, count in neighbor_counts.items():
            if cell in self.alive:
                if count == 2 or count == 3:
                    new_alive.add(cell)
            else:
                if count == 3:
                    new_alive.add(cell)

        self.alive = new_alive

    # ----------------------------
    # Image loading
    # ----------------------------
    @classmethod
    def from_image(
        cls,
        path: str,
        *,
        sample_step: int = 1,
        crop_to_content: bool = True,
    ) -> "GameOfLife":
        """
        Load image and treat ONLY pure white pixels as alive.

        (255,255,255) -> alive
        EVERYTHING ELSE -> dead
        """
        img = Image.open(path).convert("RGB")
        w, h = img.size
        px = img.load()

        alive: Set[Coord] = set()

        for y in range(0, h, sample_step):
            for x in range(0, w, sample_step):
                if px[x, y] == (255, 255, 255):
                    alive.add((x // sample_step, y // sample_step))

        life = cls(alive)

        if crop_to_content and life.alive:
            min_x = min(x for x, _ in life.alive)
            min_y = min(y for _, y in life.alive)
            life.alive = {(x - min_x, y - min_y) for (x, y) in life.alive}

        return life

    # ----------------------------
    # Helpers
    # ----------------------------
    def bounds(self) -> Optional[Tuple[int, int, int, int]]:
        if not self.alive:
            return None
        xs = [x for x, _ in self.alive]
        ys = [y for _, y in self.alive]
        return min(xs), min(ys), max(xs), max(ys)
