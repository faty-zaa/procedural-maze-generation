# Mazegen Package

## Description

`mazegen` is a standalone Python package responsible for maze generation and pathfinding logic.

It implements a Depth-First Search (DFS) algorithm using Recursive Backtracking to generate a maze structure. The package also provides shortest-path computation and export functionality.

This package is designed to be reusable and independent from display or configuration parsing logic.

---

## Main Class

### `MazeGenerator`

```python
class MazeGenerator:
    def __init__(
        self,
        width: int,
        height: int,
        entry: Tuple[int, int],
        exit: Tuple[int, int],
        perfect: bool = True,
        seed: int | None = None
    )
```

### Parameters

- `width` → Maze width (number of columns)
- `height` → Maze height (number of rows)
- `entry` → Entry coordinates `(x, y)`
- `exit` → Exit coordinates `(x, y)`
- `perfect` → If `True`, generates a perfect maze
- `seed` → Optional random seed for reproducibility

---

## Core Methods

### `carve(x: int, y: int) -> None`

Implements the DFS Recursive Backtracking algorithm to generate the maze structure.

---

### `place_42_block() -> Set[Tuple[int, int]]`

Adds special blocked cells inside the maze structure.

---

### `bfs_shortest_path() -> list`

Computes the shortest path between the entry and exit using the Breadth-First Search (BFS) algorithm.

---

### `write_output(filename: str) -> None`

Exports the maze representation to a file.

---

## Internal Structure

The maze is internally represented as a 2D grid of cells.

Each cell stores:
- Wall information (top, right, bottom, left)
- Visited state
- Additional metadata if needed

---

## Perfect vs Non-Perfect Mazes

- If `perfect=True`, the DFS algorithm generates a maze with exactly one unique path between any two points.
- If `perfect=False`, additional walls may be removed to create loops.

---

## Reusability

The package is designed to be reusable:

- Can be imported into other Python projects
- Can be extended with additional maze generation algorithms
- Can be integrated into graphical interfaces or game engines
- Fully independent from display and configuration parsing logic

Example usage:

```python
from mazegen.generator import MazeGenerator

generator = MazeGenerator(
    width=19,
    height=17,
    entry=(0, 0),
    exit=(14, 14),
    perfect=False,
    seed=24
)

generator.carve(0, 0)
path = generator.bfs_shortest_path()
generator.write_output("output.txt")
```

## Building and Installing the Package

The `mazegen` package is designed to be reusable and installable.

### Build Instructions

The package configuration is defined in `pyproject.toml`:

```toml
[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "mazegen"
version = "1.0.0"
description = "Reusable maze generator"
authors = [{name = "Moussa_Fatyza"}]
readme = "README.md"
requires-python = ">=3.10"

[tool.setuptools]
packages = ["mazegen"]
```

To build the package:

1. Install the Python build tool if not already installed:

```bash
pip install build
```

2. Build the package:

```bash
python3 -m build
```

This will generate:

- `mazegen-1.0.0-py3-none-any.whl`
- `mazegen-1.0.0.tar.gz`

---

### Install the Package

After building, install it locally:

```bash
pip install mazegen-1.0.0-py3-none-any.whl
# or
pip install mazegen-1.0.0.tar.gz
```

Once installed, the package can be imported like any other Python package:

```python
from mazegen.generator import MazeGenerator

generator = MazeGenerator(width=19, height=17, entry=(0,0), exit=(14,14))
```

You can then access all the class methods (`carve`, `bfs_shortest_path`, `write_output`, etc.) as usual.

---

### Verification

You can verify the installation with:

```bash
pip list
```

Expected output should include:

```
Package    Version
---------- -------
mazegen    1.0.0
packaging  26.0
pip        26.0.1
setuptools 82.0.0
wheel      0.46.3
```

This confirms that the `mazegen` package is installed and ready to be used in any Python project.