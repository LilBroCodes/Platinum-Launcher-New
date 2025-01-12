import json
import appdata


def get_home_folder():
    try:
        with open("config.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"home": str(appdata.get_home_folder())}
        with open("config.json", "w") as file:
            json.dump(data, file)

    return data.get("home")
