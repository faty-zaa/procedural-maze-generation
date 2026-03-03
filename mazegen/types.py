from typing import TypedDict

# TypeDict is a comming from typing
# and him work is a gev type structure for dict


class Walls(TypedDict):
    top: bool
    bottom: bool
    left: bool
    right: bool


class Cell(TypedDict):
    visited: bool
    visited_bfs: bool
    walls: Walls


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
