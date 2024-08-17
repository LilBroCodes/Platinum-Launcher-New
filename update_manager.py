import json
import os
import appdata
import requests
import zipfile
import api
from typing import List, Dict
import shutil

branch_config = {
    1: {
        "display_name": "Polzhax",
        "type": "mod",
        "mod_path": "/",
        "mod_type": "Client"
    },
    2: {
        "display_name": "GDPS",
        "type": "game"
    },
    3: {
        "display_name": "Mat's Nice Hacks",
        "type": "mod",
        "mod_path": "/",
        "mod_type": "Client"
    },
    5: {
        "display_name": "Texture Packs",
        "type": "mod",
        "mod_path": "Resources",
        "mod_type": "TPack"
    }
}

version_cache = {}


def save_version_cache():
    cache_path = os.path.join(appdata.get_home_folder(), ".platinum-launcher", "version_cache.json")
    with open(cache_path, "w") as file:
        json.dump(version_cache, file, indent=1)


def load_version_cache():
    global version_cache
    cache_path = os.path.join(appdata.get_home_folder(), ".platinum-launcher", "version_cache.json")
    if os.path.exists(cache_path):
        with open(cache_path, "r") as file:
            version_cache = json.load(file)
    else:
        version_cache = {}


def fetch_versions(branch_id: int):
    if branch_id in version_cache:
        return version_cache[branch_id]
    versions = api.get_versions(branch_id)
    version_cache[branch_id] = versions
    save_version_cache()
    return versions


def download_and_extract(version_id: int, extract_path: str, is_tpack=False):
    data = api.download(str(version_id))
    response: requests.Response = data["response"]
    zip_file_path = f"temp_{version_id}.zip"
    with open(zip_file_path, "wb") as file:
        for chunk in response.iter_content(8192):
            file.write(chunk)

    with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
        if is_tpack:
            for file_info in zip_ref.infolist():
                target_file = os.path.join(extract_path, file_info.filename)
                if os.path.exists(target_file):
                    try:
                        os.remove(target_file)
                    except PermissionError:
                        pass
        zip_ref.extractall(extract_path)

    os.unlink(zip_file_path)


def get_branch_config(branch_id: int):
    return branch_config.get(branch_id)


def change_config(game_version: int, mods: List[Dict[str, int]]):
    config_path = os.path.join(appdata.get_home_folder(), ".platinum-launcher")
    if not os.path.exists(config_path):
        os.makedirs(config_path)
    with open(os.path.join(config_path, "version.json"), "w") as file:
        file.write(json.dumps({
            "game_version": game_version,
            "mods": mods
        }, indent=1))


def load_config():
    config_path = os.path.join(appdata.get_home_folder(), ".platinum-launcher")
    if not os.path.exists(config_path):
        os.makedirs(config_path)
    try:
        with open(os.path.join(config_path, "version.json"), "r") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        return {"game_version": None, "mods": []}


def install_game_and_mods(installed_mods: List[Dict[str, int]], installed_game_version: int):
    appdata_path = os.path.join(appdata.get_home_folder(), ".platinum-launcher")
    base_path = os.path.join(appdata_path, "GDPS")

    if os.path.exists(base_path):
        shutil.rmtree(base_path)
    os.makedirs(base_path, exist_ok=True)
    download_and_extract(installed_game_version, base_path)

    for mod in installed_mods:
        mod_id = mod['id']
        branch_id = mod['branch_id']
        mod_info = get_branch_config(branch_id)
        target_path = base_path if mod_info["mod_path"] == "/" else os.path.join(base_path, mod_info["mod_path"])
        if mod_info and mod_info["type"] == "mod" and mod_info.get("mod_type") == "Client":
            download_and_extract(mod_id, target_path)

    for mod in installed_mods:
        mod_id = mod['id']
        branch_id = mod['branch_id']
        mod_info = get_branch_config(branch_id)
        target_path = base_path if mod_info["mod_path"] == "/" else os.path.join(base_path, mod_info["mod_path"])
        if mod_info and mod_info["type"] == "mod" and mod_info.get("mod_type") == "TPack":
            download_and_extract(mod_id, target_path, True)


def install_branch(branch_id: int, version_id: int):
    appdata_path = os.path.join(appdata.get_home_folder(), ".platinum-launcher")
    base_path = os.path.join(appdata_path, "GDPS")
    config = load_config()
    branch_c = get_branch_config(branch_id)

    if not branch_c:
        print(f"Branch ID {branch_id} not found in configuration.")
        return

    installed_mods = config.get("mods", [])
    installed_game_version = config.get("game_version", None)

    versions = fetch_versions(branch_id)
    if not any(version['id'] == version_id for version in versions):
        print(f"Version ID {version_id} not found in branch {branch_id}.")
        return

    if branch_c["type"] == "game":

        if os.path.exists(base_path):
            shutil.rmtree(base_path)
        os.makedirs(base_path, exist_ok=True)
        download_and_extract(version_id, base_path)

        change_config(version_id, installed_mods)

    elif branch_c["type"] == "mod":
        mod_path = branch_c["mod_path"]
        mod_type = branch_c["mod_type"]

        if mod_type == "Client":

            installed_mods = [mod for mod in installed_mods if get_branch_config(mod['branch_id']).get("mod_type") != "Client"]
            installed_mods.append({"id": version_id, "branch_id": branch_id})
            change_config(installed_game_version, installed_mods)
            install_game_and_mods(installed_mods, installed_game_version)

        elif mod_type == "TPack":

            installed_mods = [mod for mod in installed_mods if get_branch_config(mod['branch_id']).get("mod_type") != "TPack"]
            installed_mods.append({"id": version_id, "branch_id": branch_id})
            change_config(installed_game_version, installed_mods)
            install_game_and_mods(installed_mods, installed_game_version)

        else:

            download_and_extract(version_id, os.path.join(base_path, mod_path))
            installed_mods.append({"id": version_id, "branch_id": branch_id})
            change_config(installed_game_version, installed_mods)

load_version_cache()
