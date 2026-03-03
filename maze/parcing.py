"""Parse and validate configuration files for maze generation."""
import sys


def parse_config(filename: str) -> dict:
    """Read and parse the configuration file.
    
    Args:
        filename: Path to configuration file
        
    Returns:
        dict: Configuration settings as key-value pairs
    """
    config = {}
    check_duplicat = []

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
                    check_duplicat.append(key.upper().strip())
                except Exception:
                    print("The configuration file must contain one ‘KEY=VALUE‘"
                          "pair per line.")
                    sys.exit(1)
            n = len(check_duplicat)
            for i in range(n):
                for j in range(i + 1, n):
                    a = check_duplicat[i]
                    b = check_duplicat[j]
                    if a == b:
                        print(f"Error: "
                              f"Duplicate key found: '{check_duplicat[i]}'")
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


def validate_config(config: dict, filename: str) -> None:
    """Check if configuration has all required keys and valid values.
    
    Args:
        config: Configuration dictionary to validate
        filename: Name of the configuration file
    """
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

    for a in config.keys():
        is_keys.append(a)

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
    if width > 100 or height > 100:
        raise ValueError("WIDTH and HEIGHT must be < 100")

    config["WIDTH"] = width
    config["HEIGHT"] = height

# -------------------------------
# enrty : -->

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
# exit : -->
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
# -------------------------------chek output fi;le
    if config["OUTPUT_FILE"] == filename:
        raise ValueError("the config filename can't be "
                         "the same as the output filename")
    value = config["OUTPUT_FILE"].split('.', 1)
    if len(value) != 2:
        raise ValueError("Error: 'OUTPUT_FILE' value must "
                         "follow the pattern 'filename.txt'")
    if value[1] != "txt":
        raise ValueError("OUTPUT_FILE must be a '.txt' "
                         "file (Example: 'output.txt'")
