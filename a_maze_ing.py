import sys
import os
import random
import copy
from maze.parcing import parse_config, validate_config
from maze.display import display_maze_final
from mazegen.generator import MazeGenerator


def main() -> None:
    """Main function to generate and display interactive maze."""
    original_maze = None
    sys.setrecursionlimit(200000)
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        return

    config = parse_config(sys.argv[1])
    try:
        validate_config(config, sys.argv[1])
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
    try:
        blocked = gen.place_42_block()
    except ValueError as e:
        print(e)
        sys.exit(1)

    if config["ENTRY"] in blocked or config["EXIT"] in blocked:
        print("ENTRY or EXIT inside 42 block")
        return

    if config.get("SEED") is not None:
        random.seed(config["SEED"])

    x, y = config["ENTRY"]
    gen.carve(x, y)

    if not config["PERFECT"]:
        gen.break_continuous_walls()
    gen.write_output(config["OUTPUT_FILE"])
    original_maze = copy.deepcopy(gen.maze)

    b = 0
    path_on = False

    display_maze_final(
                    gen.maze,
                    config["ENTRY"],
                    config["EXIT"],
                    1,
                    0,
                    "██"
                )
    chosen_color = "██"
    while True:
        try:
            print(
                "\n"
                "╔════════════ MAZE MENU ════════════╗\n"
                "║                                   ║\n"
                "║  [1] 🎰 Generation new maze       ║\n"
                "║  [2] 🛡️ fatyza path                ║\n"
                "║  [3] 🗡️ Active Color               ║\n"
                "║  [4] 🚪 Exit                      ║\n"
                "╚═══════════════════════════════════╝\n"
            )

            choice = input("👉 Select an option [1-2-3-4]: ")

            os.system("clear")
# ------
            if choice == "1":

                gen.write_output(config["OUTPUT_FILE"])
                gen = MazeGenerator(
                    config["WIDTH"],
                    config["HEIGHT"],
                    config["ENTRY"],
                    config["EXIT"],
                    config["PERFECT"]
                )

                blocked = gen.place_42_block()

                if config["ENTRY"] in blocked or config["EXIT"] in blocked:
                    print("ENTRY or EXIT inside 42 block")
                    return
                if config.get("SEED") is not None:
                    random.seed(config["SEED"])
                gen.carve(x, y)
                if not config["PERFECT"]:
                    gen.break_continuous_walls()
                original_maze = copy.deepcopy(gen.maze)
                path_on = False
                display_maze_final(
                    gen.maze,
                    config["ENTRY"],
                    config["EXIT"],
                    1,
                    0,
                    chosen_color
                )
                b = 0
# ------
            elif choice == "2":
                if not path_on:
                    gen.maze = copy.deepcopy(original_maze)

                    path = gen.bfs_shortest_path()
                    for px, py in path:
                        gen.maze[py][px]["path"] = True

                    path_on = True
                else:
                    gen.maze = copy.deepcopy(original_maze)
                    path_on = False

                display_maze_final(
                    gen.maze,
                    config["ENTRY"],
                    config["EXIT"],
                    1 if b == 0 else 0,
                    1 if path_on else 0,
                    chosen_color
                )
# ------
            elif choice == "3":
                color_codes = ["\033[48;5;82m",
                               "\033[48;5;226m",
                               "\033[48;5;201m",
                               "\033[48;5;45m",
                               "\033[48;5;208m",
                               "\033[5;42m",
                               "\033[1;103m",
                               "\033[5;104m",
                               "\033[1;105m",
                               "\033[5;106m"]
                chosen_color = random.choice(color_codes)
                display_maze_final(
                    gen.maze,
                    config["ENTRY"],
                    config["EXIT"],
                    0,
                    1 if path_on else 0,
                    chosen_color
                )
                b = 1
# ------
            elif choice == "4":
                print("Exiting program... Goodbye!😚\nsee you later 👋")
                sys.exit(0)

            else:
                print("⚠️ Invalid choice. Please enter 1 or 2 or 3 or 4.'🤬'\n")

        except (KeyboardInterrupt, EOFError):
            print("\n\n🛑 Program interrupted. Exiting safely...")
            sys.exit(1)


if __name__ == "__main__":
    main()
