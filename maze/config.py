import sys


def parse_config(filename: str) -> dict:
    config = {}
    check_deplicat = []

    try:
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                try:
                    key, value = line.split("=", 1)
                    if value == "":
                        raise ValueError("Error")
                    config[key.upper().strip()] = value.strip()
                    check_deplicat.append(key.upper().strip())
                except Exception:
                    print("The configuration file must contain one ‘KEY=VALUE‘"
                          "pair per line.")
                    sys.exit(1)
            # print(check_deplicat)
            # look hna check dail deplicat
            n = len(check_deplicat)
            for i in range(n):
                for j in range(i + 1, n):
                    a = check_deplicat[i]
                    b = check_deplicat[j]
                    if a == b:
                        print(f"Error: "
                              f"Duplicate key found: '{check_deplicat[i]}'")
                        sys.exit(1)
            return config
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
    seed = {"SEED"}

    is_keys = []
# <<<<<<< HEAD

# =======
# >>>>>>> e39d3a50d05cc55e21c76988ba85c1eb6a291924
    for a in config.keys():
        is_keys.append(a)
    # print(is_keys)

    for a in importance_keys:
        if a not in is_keys:
            raise ValueError(f"Error: missing required key '{a}'")

    for a in is_keys:
        if a in seed:
            try:
                int(config["SEED"])
            except ValueError:
                raise ValueError("SEED must be integr Value")

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
# -------------------------------chek output fi;le

    value = config["OUTPUT_FILE"].split('.', 1)
    if len(value) != 2:
        raise ValueError("Error: 'OUTPUT_FILE' value must "
                         "follow the pattern 'filename.txt'")
    if value[1] != "txt":
        raise ValueError("OUTPUT_FILE must be a '.txt' "
                         "file (Example: 'output.txt'")
