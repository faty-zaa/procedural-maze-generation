# """maze creation + grid management"""

import random
from typing import List, Tuple, Set
from collections import deque
import sys
from mazegen.types import Maze, Cell
from typing import Optional


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
        self.blocked_cells: set[tuple[int, int]] = set()

        self.maze: Maze = self.create_maze()

    # =====================

    def create_maze(self) -> Maze:
        """Create an empty maze grid with all walls up."""
        grad = []

        for f in range(self.height):
            row = []
            for w in range(self.width):
                cell: Cell = {
                    "walls": {
                        "top": True,
                        "bottom": True,
                        "left": True,
                        "right": True
                    },
                    "visited": False,
                    "visited_bfs": False
                }
                row.append(cell)
            grad.append(row)

        return grad

    # ba3333333333333333333333333

    def _get_unvisited_neighbors(self, x: int, y: int) -> List:
        """Get list of unvisited neighbor cells."""
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

    def carve(self, x: int, y: int) -> None:
        """Carve paths through the maze recursively."""
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
        """Place a '42' ASCII art block in the center of maze."""
        blocked = set()

        if self.width <= 10 or self.height <= 10:
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
                    self.blocked_cells.add((cell_x, cell_y))

        return blocked
# --------------------------------------

    def break_continuous_walls(self) -> None:
        """Break long continuous walls to create imperfect maze."""
        for y in range(1, self.height - 1):
            wall_count = 0
            start_x = 0
            for x in range(self.width):
                if self.maze[y][x]["walls"]["bottom"]:
                    if wall_count == 0:
                        start_x = x
                    wall_count += 1
                else:
                    if wall_count >= 3:
                        mid_x = start_x + (wall_count // 2)
                        if ((mid_x, y) not in self.blocked_cells and
                                (mid_x, y + 1) not in self.blocked_cells):
                            self.maze[y][mid_x]["walls"]["bottom"] = False
                            self.maze[y+1][mid_x]["walls"]["top"] = False
                    wall_count = 0

        for x in range(1, self.width - 1):
            wall_count = 0
            start_y = 0
            for y in range(self.height):
                if self.maze[y][x]["walls"]["right"]:
                    if wall_count == 0:
                        start_y = y
                    wall_count += 1
                else:
                    if wall_count >= 3:
                        mid_y = start_y + (wall_count // 2)
                        if ((x, mid_y) not in self.blocked_cells
                                and (x+1, mid_y) not in self.blocked_cells):
                            self.maze[mid_y][x]["walls"]["right"] = False
                            self.maze[mid_y][x+1]["walls"]["left"] = False
                    wall_count = 0

# --------------------------------------

    def get_neighbors(self, x: int, y: int) -> list:
        """Get accessible neighbor cells (no walls between)."""
        neighbors = []
        cell = self.maze[y][x]
        if not cell["walls"]["top"] and y > 0:
            neighbors.append((x, y - 1))
        if not cell["walls"]["bottom"] and y < self.height - 1:
            neighbors.append((x, y + 1))
        if not cell["walls"]["left"] and x > 0:
            neighbors.append((x - 1, y))
        if not cell["walls"]["right"] and x < self.width - 1:
            neighbors.append((x + 1, y))
        return neighbors

    def _reset_bfs_visited(self) -> None:
        """Reset BFS visited flags for all cells."""
        for row in self.maze:
            for cell in row:
                cell["visited_bfs"] = False

    def bfs_shortest_path(self) -> list:
        """Find shortest path from entry to exit using BFS.
        
        Returns:
            List of coordinates (x, y) representing the path
        """
        self._reset_bfs_visited()
        start = self.entry
        end = self.exit
        is_exit = False
        queue = deque([start])
        self.maze[start[1]][start[0]]["visited_bfs"] = True
        parent: dict[
            tuple[int, int], Optional[tuple[int, int]]
        ] = {start: None}

        while queue:
            x, y = queue.popleft()
            if (x, y) == end:
                is_exit = True
                break
            for nx, ny in self.get_neighbors(x, y):
                if not self.maze[ny][nx]["visited_bfs"]:
                    queue.append((nx, ny))
                    self.maze[ny][nx]["visited_bfs"] = True
                    parent[(nx, ny)] = (x, y)

        if not is_exit:
            return []
        path = []
        new_cell: Optional[tuple[int, int]] = end
        while new_cell is not None:
            path.append(new_cell)
            new_cell = parent[new_cell]
        path.reverse()
        return path

    def write_output(self, filename: str) -> None:
        """Write maze data to output file.
        
        Args:
            filename: Path to output file
        """
        try:
            with open(filename, "w") as f:
                for y in range(self.height):
                    line = ""
                    for x in range(self.width):
                        cell = self.maze[y][x]
                        value = 0

                        if cell["walls"]["top"]:
                            value += 1
                        if cell["walls"]["right"]:
                            value += 2
                        if cell["walls"]["bottom"]:
                            value += 4
                        if cell["walls"]["left"]:
                            value += 8

                        line += format(value, "X")

                    f.write(line + "\n")

                f.write("\n")

                f.write(f"{self.entry[0]},{self.entry[1]}\n")

                f.write(f"{self.exit[0]},{self.exit[1]}\n")

                path = self.bfs_shortest_path()

                directions = ""
                for i in range(1, len(path)):
                    x1, y1 = path[i - 1]
                    x2, y2 = path[i]

                    if x2 == x1 and y2 == y1 - 1:
                        directions += "N"
                    elif x2 == x1 and y2 == y1 + 1:
                        directions += "S"
                    elif x2 == x1 + 1 and y2 == y1:
                        directions += "E"
                    elif x2 == x1 - 1 and y2 == y1:
                        directions += "W"

                f.write(directions + "\n")
        except Exception as e:
            print("Output file Error:", e.args[1])
            sys.exit(1)
# ya9der maikonch e 3ando 2 dail element
