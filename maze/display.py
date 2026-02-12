"""mlx or ascii"""


def display_maze_final(maze, entry, exit):
    height = len(maze)
    width = len(maze[0])
    # ff = 0

    BLUE_BLOCK = "\033[41m  \033[0m"
    WALL = "██"

    entry_x, entry_y = entry
    exit_x, exit_y = exit

    print("██" * (width * 2 + 1))
    for y in range(height):
        row_str = WALL
        for x in range(width):
            has_top = maze[y-1][x]["walls"]["bottom"]
            has_left = maze[y][x-1]["walls"]["right"]
            has_right = maze[y][x]["walls"]["right"]
            has_bottom = maze[y][x]["walls"]["bottom"]

            if has_top and has_bottom and has_left and has_right:
                row_str += BLUE_BLOCK
            elif x == entry_x and y == entry_y:
                row_str += "🏐"
            elif x == exit_x and y == exit_y:
                row_str += "🥅"
            else:
                row_str += "  "
            if maze[y][x]["walls"]["right"]:
                row_str += "██"
            else:
                row_str += "  "
            # break
        print(row_str)

        bottom_str = "██"
        for x in range(width):
            if maze[y][x]["walls"]["bottom"]:
                bottom_str += "██"
            else:
                bottom_str += "  "

            if (
                maze[y][x]["walls"]["right"]
                or maze[y][x]["walls"]["bottom"]
                or (y + 1 < height and maze[y+1][x]["walls"]["right"])
                or (x + 1 < width and maze[y][x+1]["walls"]["bottom"])
            ):
                bottom_str += "██"
            else:

                bottom_str += "  "
            # break
        print(bottom_str)
        # break
        # if ff == 5:
        #     break
        # ff += 1
