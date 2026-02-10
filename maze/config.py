"""parsing"""
try:
    with open("config_default.txt","r") as conf:
        content = conf.read()
        if not content.strip():
            raise Exception("Error: file is empty")
        conf.seek(0)
        line = conf.readline()
        while line:
            line = line.strip()
            if line.startswith("#") or not line:
                line = conf.readline()
                continue
            elif line and "=" not in line:
                raise ValueError("Error: invalid configuration")
            lst = line.strip().split("=")
            line = conf.readline()
        key = []
        for element in lst:
            key.append(element.strip())
        key_up = key[0].upper()
        keys = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]
        try:
            i = int(key[1])
            print(i)
        except ValueError:
            raise ValueError("Error: invalid value")
        if key_up not in keys:
            raise ValueError(f"Error: invalid key")
        print(f"{key}")
except FileNotFoundError:
    print("Error: file not found")
except ValueError as e:
    print(e)
except Exception as e:
    print(e)