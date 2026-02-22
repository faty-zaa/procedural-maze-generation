import sys


def parse_config(filename: str) -> dict:
    config = {}

    try:
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                try:
                    key, value = line.split("=", 1)
                    config[key.upper().strip()] = value.strip()
                except Exception:
                    print("The configuration file must contain one ‘KEY=VALUE‘"
                          "pair per line.")
                    sys.exit(1)
    except PermissionError as e:
        print("Error:", e.args[1])
        sys.exit(1)

    except FileNotFoundError as e:
        print("Error:", e.args[1])
        sys.exit(1)

    except Exception as e:
        print("Error:", e)
        sys.exit(1)
    return config


def validate_config(config: dict):
    importance_keys = {
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "PERFECT",
        "OUTPUT_FILE"
    }
    # print(type(importance_keys))
    is_keys = []
    for a in config.keys():
        is_keys.append(a)
    # print(is_keys)

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
# entry : -->

    entry = config["ENTRY"].split(',')
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
# exit : -->
    exit = config["EXIT"].split(',')
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
