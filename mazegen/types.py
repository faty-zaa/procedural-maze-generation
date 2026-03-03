"""Type definitions for maze structures."""
from typing import TypedDict

# TypeDict is a comming from typing



class Walls(TypedDict):
    """Represents walls around a cell (top, bottom, left, right)."""
    top: bool
    bottom: bool
    left: bool
    right: bool


class Cell(TypedDict):
    """Represents a single cell in the maze grid."""
    visited: bool
    visited_bfs: bool
    walls: Walls


# Maze is a 2D grid of cells
Maze = list[list[Cell]]

# for fytiza
# exmple

# person = {
#     "name": "Moussa",
#     "age": 25
# }
# here mypy is not knows structure of person so ..
# if i do that ..

# from typing import TypedDict

# class Person(TypedDict):
#     name: str
#     age: int

# now you can typing like that

# p: Person = {
#     "name": "Moussa",
#     "age": 25
# }
