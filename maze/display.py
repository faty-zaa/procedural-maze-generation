"""Display maze in terminal with colors and animations."""
import os
import time
from mazegen.types import Maze


def display_maze_final(
    maze: Maze,
    entry: tuple[int, int],
    exit: tuple[int, int],
    flage: int,
    p_flage: int,
    chosen_color: str
) -> None:
    """Display the maze with entry, exit, and optional path.
    
    Args:
        maze: The maze grid to display
        entry: Starting position (x, y)
        exit: Ending position (x, y)
        flage: Flag for wall display mode
        p_flage: Flag to show path or not
        chosen_color: Color code for walls
    """
    os.system("clear")
    height = len(maze)
    width = len(maze[0])

    BLUE_BLOCK = "\033[41m  \033[0m"
    BLOCK = f"{chosen_color}  \033[0m"

    if flage == 1:
        WALL = "██"
    else:
        WALL = BLOCK

    entry_x, entry_y = entry
    exit_x, exit_y = exit

    print(WALL * (width * 2 + 1))
    for y in range(height):
        row_str = WALL
        for x in range(width):
            cell = maze[y][x]
            has_top = maze[y-1][x]["walls"]["bottom"]
            has_left = maze[y][x-1]["walls"]["right"]
            has_right = maze[y][x]["walls"]["right"]
            has_bottom = maze[y][x]["walls"]["bottom"]

            if has_top and has_bottom and has_left and has_right:
                row_str += BLUE_BLOCK
                time.sleep(0.01)
            elif x == entry_x and y == entry_y:
                time.sleep(0.02)
                row_str += "👳"
            elif x == exit_x and y == exit_y:
                time.sleep(0.02)
                row_str += "🕋"
            elif cell.get("path") and p_flage != 0:
                row_str += "✨"
                print(row_str, end="\r", flush=True)
                time.sleep(0.03)
                row_str = row_str[:-1] + "🐫"
            else:
                row_str += "  "
                time.sleep(0.001)
            if maze[y][x]["walls"]["right"]:
                row_str += WALL
                time.sleep(0.001)
            else:
                row_str += "  "
        print(row_str)

        bottom_str = WALL
        for x in range(width):
            if maze[y][x]["walls"]["bottom"]:
                bottom_str += WALL
            else:
                bottom_str += "  "

            if (
                maze[y][x]["walls"]["right"]
                or maze[y][x]["walls"]["bottom"]
                or (y + 1 < height and maze[y+1][x]["walls"]["right"])
                or (x + 1 < width and maze[y][x+1]["walls"]["bottom"])
            ):
                bottom_str += WALL
            else:

                bottom_str += "  "
        print(bottom_str)
