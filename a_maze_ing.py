import sys
from maze.config import parse_config, validate_config
from maze.display import display_maze_final
from mazegen.generator import MazeGenerator


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        return

    config = parse_config(sys.argv[1])

    try:
        validate_config(config)
    except Exception as e:
        print(e)
        return

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
        return

    x, y = config["ENTRY"]
    gen.carve(x, y)
    display_maze_final(gen.maze, config["ENTRY"], config["EXIT"])
    # print(gen.maze)


if __name__ == "__main__":
    main()
