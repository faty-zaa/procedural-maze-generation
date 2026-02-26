import sys
from maze.config import parse_config, validate_config
from maze.display import display_maze_final
from mazegen.generator import MazeGenerator


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    config = parse_config(sys.argv[1])
    # print(type(config))
    # print(config)

    try:
        validate_config(config)
    except Exception as e:
        print(e)
        sys.exit(1)

    gen = MazeGenerator(
        config["WIDTH"],
        config["HEIGHT"],
        config["ENTRY"],
        config["EXIT"],
        config["PERFECT"]
    )

    blocked = gen.place_42_block()
    # print(type(blocked))
    # print(blocked)
    if config["ENTRY"] in blocked or config["EXIT"] in blocked:
        print("ENTRY or EXIT inside 42 block")
        sys.exit(1)

    x, y = config["ENTRY"]
    gen.carve(x, y)
    path = gen.bfs_shortest_path()
    for x, y in path:
        gen.maze[y][x]["path"] = True
    display_maze_final(gen.maze, config["ENTRY"], config["EXIT"])
    # print(gen.maze)


if __name__ == "__main__":
    main()
