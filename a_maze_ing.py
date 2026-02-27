import sys
import os
import random
from maze.config import parse_config, validate_config
from maze.display import display_maze_final
from mazegen.generator import MazeGenerator


def main():
    sys.setrecursionlimit(200000)
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        return

    config = parse_config(sys.argv[1])
    # print(config)
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
    if config["ENTRY"] in blocked or config["EXIT"] in blocked:
        print("ENTRY or EXIT inside 42 block")
        return

    if config.get("SEED") is not None:
        random.seed(config["SEED"])
        # get kat9leb f dict ila l9at key mzain ila ml9atouch
        # katrje3 Nono mhm makata3tich crach wla key error
        # mli kandir random.seed(number) hna kanbadel f
        # library f ldakhel dailha wahed object -->>
        # '_global_random = Random()' donc kiatbdel
        # ghir global random generator dail library
    x, y = config["ENTRY"]
    gen.carve(x, y)
    # hna alme3alem fin machi perfect
    if not config["PERFECT"]:
        gen.add_loops(6)

    while True:
        try:
            print(
                "\n"
                "╔════════════ MAZE MENU ════════════╗\n"
                "║                                   ║\n"
                "║  [1] 🧩 Display Final Maze        ║\n"
                "║  [2] 🎰 Generation new maze       ║\n"
                "║  [3] 💋 Active Colore             ║\n"
                "║  [4] 🛡️ 🗡️ fatyza path            ║\n"
                "║  [5] 🚪 Exit                      ║\n"
                "╚═══════════════════════════════════╝\n"
            )

            choice = input("👉 Select an option [1-2-3-4]: ")

            os.system("clear")

            if choice == "1":
                display_maze_final(
                    gen.maze,
                    config["ENTRY"],
                    config["EXIT"],
                    1
                )

            elif choice == "2":

                if config.get("SEED") is not None:
                    random.seed(config["SEED"])
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

                gen.carve(x, y)
                if not config["PERFECT"]:
                    gen.add_loops(6)

                display_maze_final(
                    gen.maze,
                    config["ENTRY"],
                    config["EXIT"],
                    1
                )
            elif choice == "3":
                display_maze_final(
                    gen.maze,
                    config["ENTRY"],
                    config["EXIT"],
                    0
                )
            elif choice == "4":
                print("\n👋 Exiting program... Goodbye!😚\n")
                sys.exit(0)

            else:
                print("⚠️ Invalid choice. Please enter 1 or 2 or .'🤬'\n")

        except (KeyboardInterrupt, EOFError):
            print("\n\n🛑 Program interrupted. Exiting safely...")
            sys.exit(1)


if __name__ == "__main__":
    main()
