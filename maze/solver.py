import random
from collections import deque
from typing import List, Tuple, Dict

Cell = Dict[str, object]
Maze = List[List[Cell]]


class MazeGenerator:
    def __init__(self, width: int, height: int, entry: Tuple[int, int], exit: Tuple[int, int]):
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit

        self.maze = self.create_maze()

    def create_maze(self) -> Maze:
        grad = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                cell = {
                    "walls": {"top": True, "bottom": True, "left": True, "right": True},
                    "visited": False,
                    "visited_bfs": False
                }
                row.append(cell)
            grad.append(row)
        return grad

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

    def get_neighbors(self, x: int, y: int):
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

    def bfs_shortest_path(self):
        start = self.entry
        end = self.exit
        queue = deque([start])
        self.maze[start[1]][start[0]]["visited_bfs"] = True
        parent = {start: None}

        while queue:
            x, y = queue.popleft()
            if (x, y) == end:
                break
            for nx, ny in self.get_neighbors(x, y):
                if not self.maze[ny][nx]["visited_bfs"]:
                    queue.append((nx, ny))
                    self.maze[ny][nx]["visited_bfs"] = True
                    parent[(nx, ny)] = (x, y)
        path = []
        cell = end
        while cell is not None:
            path.append(cell)
            cell = parent[cell]
        path.reverse()
        return path
# mg = MazeGenerator(5, 5, entry=(0, 0), exit=(4, 4))
# mg.carve(0, 0)  
# path = mg.bfs_shortest_path()
# print("Shortest path:", path)