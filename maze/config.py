import sys
import random


def main():
    sys.setrecursionlimit(200000)  # i should understand this
    try:
        print(f"Config file loaded: <{sys.argv[1]}>\n")

    except IndexError:
        print("Error: missing configuration file !")
        exit()

    config = parse_config(sys.argv[1])

    try:
        validate_config(config)
    except (ValueError, IndexError)as e:
        print(e)
        exit()

    print("Config validated successfully!")
    maze = create_maze(config["WIDTH"], config["HEIGHT"])
    try:
        blocked_cells = place_42_block(maze)
        if config["ENTRY"] in blocked_cells:
            print("Error: ENTRY inside 42 block")
            exit()

        if config["EXIT"] in blocked_cells:
            print("Error: EXIT inside 42 block")
            exit()
    except ValueError as e:
        print(e)
        exit()

    x, y = config["ENTRY"]
    carve_maze(maze, x, y)
    display_maze_final(maze, config["ENTRY"], config["EXIT"])


def parse_config(filename):
    confing = {}
    try:
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                a, b = line.split('=', 1)
                confing[a.upper().strip()] = b.strip()
        return confing
    except Exception as e:
        print("Error:", e.args[0])
        sys.exit()


def validate_config(config):
    importance_keys = {
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "PERFECT",
        "OUTPUT_FILE"
    }

    is_keys = []
    for a in config:
        is_keys.append(a)

    for a in importance_keys:
        if a not in is_keys:
            raise ValueError(f"Error: missing required key '{a}'")

    try:
        width = int(config["WIDTH"])
        height = int(config["HEIGHT"])
    except ValueError:
        raise ValueError("WIDTH and HEIGHT must be just integers")

    if width <= 0 or height <= 0:
        raise ValueError("WIDTH and HEIGHT must be > 0")

    config["WIDTH"] = width
    config["HEIGHT"] = height

# -------------------------------

    entry = config["ENTRY"].split(',', 1)
    if len(entry) != 2:
        raise ValueError("ENTRY must be in format x,y")

    try:
        x = int(entry[0])
        y = int(entry[1])

    except ValueError:
        raise ValueError(f"value is not int in {entry}!")

    except IndexError:
        raise IndexError(f"Error in entry {entry} check again!")

    if x >= width or x < 0:
        raise ValueError("'x' in entry out of width")

    if y >= height or y < 0:
        raise ValueError("'y' in entry out of height")

    coord = (x, y)
    config["ENTRY"] = coord

# ----------------------------------------------------

    exit = config["EXIT"].split(',', 1)
    if len(exit) != 2:
        raise ValueError("EXIT must be in format x,y")
    try:
        x = int(exit[0])
        y = int(exit[1])

    except ValueError:
        raise ValueError(f"value is not int in {entry}!")

    except IndexError:
        raise IndexError(f"Error in {entry} check again!")

    if x >= width or x < 0:
        raise ValueError("'x' in exit out of width")

    if y >= height or y < 0:
        raise ValueError("'y' exit out of height")

    coord = (x, y)
    config["EXIT"] = coord

# --------------------------------------

    if config["ENTRY"] == config["EXIT"]:
        raise ValueError("ENTRY and EXIT must be different")

# --------------------------------------

    if config["PERFECT"].upper() == "TRUE":
        config["PERFECT"] = True
    elif config["PERFECT"].upper() == "FALSE":
        config["PERFECT"] = False
    else:
        raise ValueError("PERFECT must be 'True' or 'False'")

# =====================================


def create_maze(width, height):
    grad = []

    for f in range(height):
        row = []
        for w in range(width):
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


def get_unvisited_neighbors(maze, x, y):
    neighbors = []

    height = len(maze)
    width = len(maze[0])

    if y > 0 and not maze[y - 1][x]["visited"]:
        neighbors.append(("top", x, y - 1))

    if y < height - 1 and not maze[y + 1][x]["visited"]:
        neighbors.append(("bottom", x, y + 1))

    if x > 0 and not maze[y][x - 1]["visited"]:
        neighbors.append(("left", x - 1, y))

    if x < width - 1 and not maze[y][x + 1]["visited"]:
        neighbors.append(("right", x + 1, y))
    return neighbors

# ===========================================


def place_42_block(maze):
    blocked = set()
    height = len(maze)
    width = len(maze[0])

    if width < 10 or height < 5:
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

    start_y = height // 2 - art_h // 2
    start_x = width // 2 - art_w // 2

    for y in range(art_h):
        for x in range(len(art_42[y])):
            if art_42[y][x] == "█":
                cell_y = start_y + y
                cell_x = start_x + x
                maze[cell_y][cell_x]["visited"] = True
                blocked.add((cell_x, cell_y))
    return blocked


# ========================================


def carve_maze(maze, x, y):
    maze[y][x]["visited"] = True
    neighbors = get_unvisited_neighbors(maze, x, y)
    while neighbors:
        chosen_neighbor = random.choice(neighbors)
        direction, a, b = chosen_neighbor

        if direction == "top":
            maze[y][x]["walls"]["top"] = False
            maze[b][a]["walls"]["bottom"] = False

        elif direction == "bottom":
            maze[y][x]["walls"]["bottom"] = False
            maze[b][a]["walls"]["top"] = False

        elif direction == "left":
            maze[y][x]["walls"]["left"] = False
            maze[b][a]["walls"]["right"] = False

        elif direction == "right":
            maze[y][x]["walls"]["right"] = False
            maze[b][a]["walls"]["left"] = False
        carve_maze(maze, a, b)
        neighbors = get_unvisited_neighbors(maze, x, y)


def display_maze_final(maze, entry, exit):
    height = len(maze)
    width = len(maze[0])
    ff = 0

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

            if (maze[y][x]["walls"]["right"] or
                maze[y][x]["walls"]["bottom"] or
                (y + 1 < height and maze[y+1][x]["walls"]["right"]) or
                (x + 1 < width and maze[y][x+1]["walls"]["bottom"])):
                bottom_str += "██"
            else:
                bottom_str += "  "
            # break
        print(bottom_str)
        # break
        # if ff == 5:
        #     break
        # ff += 1


if __name__ == "__main__":
    main()
