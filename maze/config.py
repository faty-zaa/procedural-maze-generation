"""parsing"""
import sys

def ft_parsing(filename):
    try:
        "OPENING THE FILE THAT CONTAIN THE CONFIGURATION"
        with open(filename, "r") as file:
            content = file.read()
            if not content.strip():
                raise Exception("Error: file is empty")
            "RESET THE OFFSET OF THE I/O SYSTEM CALLS"
            file.seek(0)
            lines = []
            line = file.readline()
            "CHECK LINE BY LINE"
            while line:
                line = line.strip()
                "SKIPPING THE COMMENTED AND EMPTY LINES"
                if line.startswith("#") or not line:
                    line = file.readline()
                    continue
                    "CHECK IF THE LINE ELIGIBLE TO PARSE"
                elif line and "=" not in line:
                    raise ValueError("Error: invalid configuration")
                lst = line.split("=", 1)
                "SPLITING THE LINE TO WORDS AND PUT THEM IN LISt"
                key = []
                for element in lst:
                    key.append(element.strip())
                "PUT LINES AS LISTS IN ONE LIST"
                lines.append(key)
                line = file.readline()
            keys = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]
            for key in lines:
                "CHECK EVERY FIRST STRING IN EVERY LIST IN LINES LIST IF IT IS VALID KEYWORD OR NOT"
                key_up = key[0].upper()
                "CHECK DUPLICATED && INVALID KEYS"
                keys_only = [line[0].upper() for line in lines]
                if len(keys_only) != len(set(keys_only)):
                    raise ValueError("Error: duplicated key")
                elif key_up not in keys:
                    raise ValueError("Error: invalid key")
                elif len(lines) < len(keys):
                    raise ValueError("Error: missing key")
                "CHECK THE HEIGHT AND THE WIDTH VALIDITY"
                try:
                    if key_up == "WIDTH" or key_up == "HEIGHT":
                        i = int(key[1])
                except ValueError:
                    raise ValueError("Error: invalid format : key = value")
                "CHECK THE ENTRY COORDINATES VALIDITY"
                try:
                    entry_pnt = []
                    if key_up == "ENTRY":
                        enter = key[1].split(",", 1)
                        for element in enter:
                            entry_pnt.append(element.strip())
                        if len(entry_pnt) < 2:
                            raise Exception("Error: entry format must be like : (x, y)")
                        x1 = int(entry_pnt[0])
                        y1 = int(entry_pnt[1])
                        if x1 < 0 or y1 < 0:
                            raise ValueError("Error: entry can't be negative")
                except ValueError:
                    raise ValueError("Error:invalid  entry coordinates (x, y)")
                "CHECK THE EXIT COORDINATES VALIDITY"
                try:
                    exit_pnt = []
                    if key_up == "EXIT":
                        exitt = key[1].split(",", 1)
                        for element in exitt:
                            exit_pnt.append(element.strip())
                        if len(exit_pnt) < 2:
                            raise Exception("Error: exit format must be like : (x, y)")
                        x2 = int(exit_pnt[0])
                        y2 = int(exit_pnt[1])
                        if x2 < 0 or y2 < 0:
                            raise ValueError("Error: exit can't be negative")
                except ValueError:
                    raise ValueError("Error: invalid exit coordinates (x, y)")
                "CHECK THE OUTPUT FILE NAME"
                if key_up == "OUTPUT_FILE":
                    if key[1] not in ["maze.txt"]:
                        raise ValueError("Error: invalid output file")
                "CHECK THE MAZE PERFECTION"
                if key_up == "PERFECT":
                    if key[1] != "True" and key[1] != "False":
                        raise ValueError("Error: you have two choices -> True or False")
                print(f"{key}")
    except FileNotFoundError:
        print("Error: file not found")
    except ValueError as e:
        print(e)
    except Exception as e:
        print(f"Error: {e.args[1]}")


if __name__ == "__main__":
    try:
        ft_parsing(sys.argv[1])
    except IndexError:
        print("Error: messing file")
