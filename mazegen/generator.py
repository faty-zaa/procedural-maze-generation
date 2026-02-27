# """maze creation + grid management"""

import random
from typing import List, Tuple, Dict, Set

Cell = Dict[str, object]
Maze = List[List[Cell]]


class MazeGenerator:
    """
    Maze generator using recursive backtracking.
    """

    def __init__(
        self,
        width: int,
        height: int,
        entry: Tuple[int, int],
        exit: Tuple[int, int],
        perfect: bool = True,
        seed: int | None = None
    ):
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect

        # if seed is not None:
        #     random.seed(seed)

        self.maze: Maze = self.create_maze()
        # print(type(self.maze))

    # =====================

    def create_maze(self) -> Maze:
        grad = []

        for f in range(self.height):
            row = []
            for w in range(self.width):
                cell = {
                    "walls": {
                        "top": True,
                        "bottom": True,
                        "left": True,
                        "right": True
                    },
                    "visited": False
                }
                row.append(cell)
            grad.append(row)

        return grad

    # ba3333333333333333333333333

    def _get_unvisited_neighbors(self, x: int, y: int):
        neighbors = []

        if y > 0 and not self.maze[y - 1][x]["visited"]:
            neighbors.append(("top", x, y - 1))
        if y < self.height - 1 and not self.maze[y + 1][x]["visited"]:
            neighbors.append(("bottom", x, y + 1))
        if x > 0 and not self.maze[y][x - 1]["visited"]:
            neighbors.append(("left", x - 1, y))
        if x < self.width - 1 and not self.maze[y][x + 1]["visited"]:
            neighbors.append(("right", x + 1, y))

        return neighbors

    # ba33333333333333333333333333

    def carve(self, x: int, y: int):
        self.maze[y][x]["visited"] = True
        neighbors = self._get_unvisited_neighbors(x, y)

        while neighbors:
            direction, nx, ny = random.choice(neighbors)

            if direction == "top":
                self.maze[y][x]["walls"]["top"] = False
                self.maze[ny][nx]["walls"]["bottom"] = False
            elif direction == "bottom":
                self.maze[y][x]["walls"]["bottom"] = False
                self.maze[ny][nx]["walls"]["top"] = False
            elif direction == "left":
                self.maze[y][x]["walls"]["left"] = False
                self.maze[ny][nx]["walls"]["right"] = False
            elif direction == "right":
                self.maze[y][x]["walls"]["right"] = False
                self.maze[ny][nx]["walls"]["left"] = False

            self.carve(nx, ny)
            neighbors = self._get_unvisited_neighbors(x, y)

    # =====================

    def place_42_block(self) -> Set[Tuple[int, int]]:
        blocked = set()

        if self.width < 10 or self.height < 5:
            raise ValueError("Maze too small to place 42")

        art_42 = [
            "█   ███",
            "█     █",
            "███ ███",
            "  █ █",
            "  █ ███",
        ]

        art_h = len(art_42)
        art_w = max(len(row) for row in art_42)

        start_y = self.height // 2 - art_h // 2
        start_x = self.width // 2 - art_w // 2

        for y in range(art_h):
            for x in range(len(art_42[y])):
                if art_42[y][x] == "█":
                    cell_y = start_y + y
                    cell_x = start_x + x
                    self.maze[cell_y][cell_x]["visited"] = True
                    blocked.add((cell_x, cell_y))

        return blocked
# hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh

    def add_loops(self, extra_walls):
        height = self.height
        width = self.width

        removed = 0

        while removed < extra_walls:
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)

            directions = []

            if y > 0:
                directions.append(("top", x, y - 1))
            if y < height - 1:
                directions.append(("bottom", x, y + 1))
            if x > 0:
                directions.append(("left", x - 1, y))
            if x < width - 1:
                directions.append(("right", x + 1, y))

            direction, nx, ny = random.choice(directions)

            if direction == "top" and self.maze[y][x]["walls"]["top"]:
                self.maze[y][x]["walls"]["top"] = False
                self.maze[ny][nx]["walls"]["bottom"] = False
                removed += 1

            elif direction == "bottom" and self.maze[y][x]["walls"]["bottom"]:
                self.maze[y][x]["walls"]["bottom"] = False
                self.maze[ny][nx]["walls"]["top"] = False
                removed += 1

            elif direction == "left" and self.maze[y][x]["walls"]["left"]:
                self.maze[y][x]["walls"]["left"] = False
                self.maze[ny][nx]["walls"]["right"] = False
                removed += 1

            elif direction == "right" and self.maze[y][x]["walls"]["right"]:
                self.maze[y][x]["walls"]["right"] = False
                self.maze[ny][nx]["walls"]["left"] = False
                removed += 1
