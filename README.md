*This project has been created as part of the 42 curriculum by msbayihi, falamlih.*

# A-Maze-ing 🧩

## Description

A-Maze-ing is a Python project that generates a grid-based maze composed of walls and paths, with a defined entry and exit point. The objective is not only to generate the maze but also to compute the shortest path between the entry and exit.

The maze is fully configurable through a `config.txt` file, allowing users to define dimensions, generation type, entry/exit coordinates, and reproducibility options.

The maze is displayed using ASCII characters directly in the terminal.

### Features

- ASCII maze display
- Configurable width and height
- Entry and exit points
- Shortest path solving
- Perfect maze generation (unique path between any two points)
- Non-perfect maze generation (loops allowed)
- Reproducible generation using a random seed
- Export to output file
- Modular package-based architecture

---

## Instructions

### Requirements

- Python 3.10+
- Make
- pip (for package building)

---

### Running the Project

To execute the project:

```bash
make run
```

This runs:

```bash
python3 a_maze_ing.py config.txt
```

The program reads the configuration file, generates the maze, computes the shortest path, and displays the result in the terminal.

---

### Building the Maze Generator Package

The maze generation logic is implemented as a reusable Python package located in the `mazegen/` directory.

To build the package:

```bash
pip install build
python3 -m build
```

This generates:

- `mazegen-1.0.0.tar.gz`
- `mazegen-1.0.0-py3-none-any.whl`

The package can then be reused in other Python projects.

---

## Configuration File Structure

Example `config.txt`:

```
HEIGHT = 17
WIDTH = 19

PERFECT = false
SEED = 24

ENTRY = 0,0
EXIT = 14,14

OUTPUT_FILE = output.txt
```

### Parameters

- **HEIGHT** → Number of rows (must be > 0)
- **WIDTH** → Number of columns (must be > 0)
- **PERFECT** → `true` or `false`
- **SEED** → Integer for reproducible generation
- **ENTRY** → Coordinates in format `x,y`
- **EXIT** → Coordinates in format `x,y`
- **OUTPUT_FILE** → Output file name

### Validation Rules

- Dimensions must be positive integers
- Entry and exit must be inside maze boundaries
- Seed must be an integer
- Perfect must be boolean

---

## Maze Generation Algorithm

The maze generation is based on **Depth-First Search (DFS)** using the **Recursive Backtracking** technique.

### Algorithm Steps

1. Start from an initial cell.
2. Mark it as visited.
3. Randomly choose an unvisited neighbor.
4. Remove the wall between cells.
5. Recursively continue.
6. Backtrack when no neighbors are available.

This guarantees a **perfect maze**, meaning exactly one unique path exists between any two points.

### Non-Perfect Maze

When `PERFECT = false`, an additional method randomly removes extra walls after generation.  
This introduces loops, allowing multiple paths between points.

---

## Why We Chose This Algorithm

We selected Recursive Backtracking because:

- It is simple and reliable.
- It guarantees perfect maze generation.
- It is memory-efficient.
- It produces natural-looking maze structures.
- It is easily extendable to support loop creation.

---

## Reusable Components

The project is modular and structured as a reusable package.

Reusable parts:

- `MazeGenerator` class
- DFS generation logic
- Loop-adding method
- Cell and wall structure management

The generator can be reused in:

- Other Python applications
- Graphical interfaces
- Game engines
- Algorithm visualization tools

The architecture separates:

- Generation logic (`mazegen/`)
- Display logic (`maze/display.py`)
- Configuration parsing (`maze/parcing.py`)
- Application entry point (`a_maze_ing.py`)

---

## Project Structure

```
.
├── Makefile
├── README.md
├── a_maze_ing.py
├── config.txt
├── maze/
│   ├── __init__.pymazegen-1.0.0-py3-none-any.whl
│   ├── display.py
│   └── parcing.py
├── mazegen/
│   ├── README.md
│   ├── __init__.py
│   ├── generator.py
│   └── types.py
├── mazegen-1.0.0-py3-none-any.whl
├── mazegen-1.0.0.tar.gz
└── pyproject.toml
```

---

## Team & Project Management

### Roles

- **msbayihi**
  - Maze generation algorithm (DFS)
  - Loop creation logic
  - Perfect maze implementation

- **falamlih**
  - Shortest path algorithm (entry to exit)

- **Shared Responsibilities**
  - Configuration parsing
  - ASCII display
  - Initial project structure design
  - Output file handling

---

### Planning & Workflow

We started by designing the project structure and defining the required files and package organization.

We worked using Git with three branches:

- `main`
- `msbayihi`
- `falamlih`

Each member developed features on their own branch.  
Changes were merged into `main` only after discussion and validation.

---

### What Worked Well

- Clear separation of responsibilities
- Modular architecture
- Efficient Git workflow with branch management
- Strong collaboration during parsing and display implementation

---

### What Could Be Improved

- Earlier integration testing
- More formal task planning before coding
- Adding automated tests

---

### Tools Used

- Git & GitHub
- Make
- Python packaging tools
- VS Code
- AI assistance (used for structure review, documentation guidance, and debugging support)

---

## Resources

- Python Official Documentation
- Depth-First Search (DFS) algorithm references
- Recursive Backtracking maze generation articles
- Python packaging documentation (`pyproject.toml`)
- Git branching workflow documentation

AI was used mainly for:
- Reviewing structure
- Improving documentation clarity
- Debugging guidance
- README organization