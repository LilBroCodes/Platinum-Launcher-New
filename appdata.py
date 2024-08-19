import json


def get_home_folder():
    with open("config.json", "r") as file:
        data = json.load(file)

    return data.get("home")
