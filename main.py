import threading
import _thread
from PIL import Image
import tkinter as tk
import customtkinter as ctk

from typing import List, Dict, Any
import os
import appdata

from dialogue import info_popup
import api
import update_manager
import gd
import middleman

texture_pack_option_menu = None
mod_option_menu = None
version_option_menu = None
middleman_enabled = False
root = None


def launch():
    config_path = appdata.get_home_folder()
    gdps_path = os.path.join(config_path, "GDPS")
    exe_path = os.path.join(gdps_path, "PlatinumGDPS.exe")
    if os.path.exists(exe_path):
        print(f"#DEBUG | Launching GDPS at {exe_path}")
        gd_thread = threading.Thread(target=gd.universal_exec_open, args=(exe_path, [], gdps_path))
        gd_thread.start()
        if middleman_enabled:
            proxy_thread = threading.Thread(target=middleman.run_server, args=())
            proxy_thread.start()
    else:
        info_popup(text="GDPS Not Installed.", title="Error", close="Ok", height=150, popup_type="textOnly")


def creds():
    data = """
        Songs:
            Flourish (Platinum Pack Menu Theme) - Purrple Cat

        Images:
            Main icon - Zud
            Custom BG (Ingame, Platinum Pack) - Zud

        Mods:
            PolzHax - Pololak (https://github.com/Pololoak)
            Mat's nice hacks - matcool (https://github.com/matcool)

        Misc:
            Poggers hosting service - Jean
            Account proxy (node.js version) - Jean
    """
    info_popup("textOnly", "Credits", text=data, do_exit=False, width=450, height=400, font_family="Roboto Medium")


def version_selector(data: List[Dict[str, Any]], root: ctk.ctk_tk, w: int, h: int, placeholder: str):
    dnames = [version["version_number"] for version in data]
    dnames.insert(0, placeholder)
    return ctk.CTkOptionMenu(root, width=w, height=h, values=dnames, fg_color="#333333",
                             dropdown_fg_color="#333333", dropdown_hover_color="#595959", button_color="#333333",
                             button_hover_color="#595959", corner_radius=5, dropdown_font=("Roboto Medium", 12))


def mod_selector(root: ctk.ctk_tk, w: int, h: int):
    mod_options = ["None", "PolzHax", "Mat's Nice Hacks"]
    return ctk.CTkOptionMenu(root, width=w, height=h, values=mod_options, fg_color="#333333",
                             dropdown_fg_color="#333333", dropdown_hover_color="#595959", button_color="#333333",
                             button_hover_color="#595959", corner_radius=5, dropdown_font=("Roboto Medium", 12))


def texture_pack_selector(root: ctk.ctk_tk, w: int, h: int, data: List[Dict[str, Any]]):
    dnames = []
    for version in data:
        if version.get("display_name"):
            dnames.append(version["display_name"])
        else:
            dnames.append(version["version_number"])
    dnames.insert(0, "None")
    return ctk.CTkOptionMenu(root, width=w, height=h, values=dnames, fg_color="#333333",
                             dropdown_fg_color="#333333", dropdown_hover_color="#595959", button_color="#333333",
                             button_hover_color="#595959", corner_radius=5, dropdown_font=("Roboto Medium", 12))


def download_version(version):
    game_versions = api.get_versions(2)
    version_data = [idx for idx in game_versions if idx["version_number"] == version]
    id = version_data[0]["id"]
    update_manager.install_branch(2, id)
    mod_option_menu.configure(state="normal")
    texture_pack_option_menu.configure(state="normal")


def configure(popup=True):
    global texture_pack_option_menu
    global mod_option_menu
    global version_option_menu
    global middleman_enabled

    game_version_number = version_option_menu.get()
    versions = api.get_versions(2)
    version = [i for i in versions if i.get("version_number") == game_version_number]
    game_version = version[0].get("id")
    mods = []

    if texture_pack_option_menu.get() != "None":
        tpack_version_number = texture_pack_option_menu.get()
        versions = api.get_versions(5)
        version = [i for i in versions if i.get("display_name") == tpack_version_number]
        data = {
            "id": int(version[0].get("id")),
            "branch_id": 5
        }
        mods.append(data)
    if mod_option_menu.get() == "PolzHax":
        mod_version_number = mod_option_menu.get()
        versions = api.get_versions(1)
        versions.sort(key=lambda x: x["id"], reverse=True)
        data = {
            "id": int(versions[0].get("id")),
            "branch_id": 1
        }
        mods.append(data)
    if mod_option_menu.get() == "Mat's Nice Hacks":
        mod_version_number = mod_option_menu.get()
        versions = api.get_versions(3)
        versions.sort(key=lambda x: x["id"], reverse=True)
        data = {
            "id": int(versions[0].get("id")),
            "branch_id": 3
        }
        mods.append(data)

    version_data = version[0]
    middleman_enabled = True if version_data["middleman"] == 1 else False
    update_manager.change_config(game_version, mods, middleman_enabled)

    if popup:
        info_popup("textOnly", "Info", text="Saved config.", do_exit=False, width=200, height=150,
                   font_family="Roboto Medium", close="Ok")

    return mods, game_version


def download():
    mods, game_version = configure(False)

    def run_and_popup():
        update_manager.install_game_and_mods(mods, game_version)
        root.after(0, lambda: info_popup("textOnly", "Info", text="Download complete.", do_exit=False, width=200,
                                         height=150,
                                         font_family="Roboto Medium", close="Ok"))
        root.after(0, load)

    thread = threading.Thread(target=run_and_popup)
    thread.start()
    info_popup("textOnly", "Info", text="Downloading game and mods...", do_exit=False, width=200, height=150,
               font_family="Roboto Medium", close="Ok")


def load():
    global texture_pack_option_menu
    global mod_option_menu
    global version_option_menu
    config = update_manager.load_config()
    if config.get("game_version") is not None:
        game_version = config.get("game_version")
        versions = api.get_versions(2)
        version = [i for i in versions if i.get("id") == game_version]
        version = version[0]
        version_option_menu.set(version.get("version_number"))
        print(f"#DEBUG | Loaded game version {version.get('version_number')}, data {version}")
        mod_option_menu.configure(state="normal")
        texture_pack_option_menu.configure(state="normal")
    for mod in config.get("mods"):
        mod_id = mod["id"]
        branch_id = mod["branch_id"]
        branch_info = update_manager.get_branch_config(branch_id)
        versions = api.get_versions(branch_id)
        version = [i for i in versions if i.get("id") == mod_id]
        version = version[0]
        display_name = "PolzHax" if branch_id == 1 else version.get("display_name")
        if display_name == "":
            display_name = "Mat's Nice Hacks" if branch_id == 3 else version.get("display_name")
        if branch_info["type"] == "mod" and branch_info.get("mod_type") == "TPack":
            print(f"#DEBUG | Loaded mod {display_name}, version {version}")
            texture_pack_option_menu.set(display_name)
        if branch_info["type"] == "mod" and branch_info.get("mod_type") == "Client":
            print(f"#DEBUG | Loaded mod {display_name}, version {version}")
            mod_option_menu.set(display_name)


def main():
    global root
    root = ctk.CTk()
    root.title("Platinum GDPS Launcher")
    root.geometry("1000x750")
    root.iconbitmap("data/icon.png")
    img = tk.PhotoImage(file="data/icon.png")
    root.tk.call('wm', 'iconphoto', root._w, img)

    font_family = "Roboto Medium"

    bottom_frame = ctk.CTkFrame(root, height=50, bg_color="#333333", border_width=0)
    bottom_frame.pack(side="bottom", fill="x")

    top_frame = ctk.CTkFrame(root, height=50, bg_color="#333333", border_width=0)
    top_frame.pack(side="top", fill="x")

    text_label = ctk.CTkLabel(bottom_frame, text="Made by LilBroCodes & Zud", font=(font_family, 16),
                              text_color="#909090")
    text_label.pack(side="left", padx=10, pady=10)

    version_label = ctk.CTkLabel(bottom_frame, text="Platinum GDPS Launcher 1.12b", font=(font_family, 16),
                                 text_color="#909090")
    version_label.pack(side="right", padx=10, pady=10)

    launch_button = ctk.CTkButton(top_frame, text="Launch", font=(font_family, 20), text_color="white",
                                  fg_color="#444444",
                                  hover_color="#555555", width=120, height=50, command=launch)
    launch_button.pack(side="right", padx=5)

    main_frame = ctk.CTkFrame(master=root, width=1920, height=1080, fg_color="#333333")
    main_frame.pack(anchor=ctk.CENTER, padx=10, pady=10, expand=True)

    image_path = "data/icon.png"
    plaster_image = ctk.CTkImage(Image.open(image_path), size=(50, 50))
    plaster = ctk.CTkButton(master=top_frame, text="", image=plaster_image, bg_color="#333333", fg_color="#333333",
                            border_color="#333333", hover_color="#333333", width=50)
    plaster.pack(padx=10, side="left")

    credits_button = ctk.CTkButton(top_frame, text="Credits", font=(font_family, 20), text_color="white",
                                   fg_color="#444444",
                                   hover_color="#555555", width=50, height=50, command=creds)
    credits_button.pack(side="left", padx=5)

    download_version_button = ctk.CTkButton(main_frame, text="Download Version", font=(font_family, 16),
                                            text_color="white",
                                            fg_color="#444444", hover_color="#555555", command=lambda: download())
    download_version_button.pack(pady=20)

    global mod_option_menu
    global texture_pack_option_menu
    global version_option_menu

    version_option_menu = version_selector(api.get_versions(2), main_frame, 300, 40, "Select Version")
    version_option_menu.pack(pady=10)

    mod_option_menu = mod_selector(main_frame, 300, 40)
    mod_option_menu.pack(pady=10)
    mod_option_menu.configure(state="disabled")

    tp_data = api.get_versions(5)
    texture_pack_option_menu = texture_pack_selector(main_frame, 300, 40, data=tp_data)
    texture_pack_option_menu.pack(pady=10)
    texture_pack_option_menu.configure(state="disabled")

    config_button = ctk.CTkButton(main_frame, text="Save Config", font=(font_family, 16),
                                  text_color="white",
                                  fg_color="#444444", hover_color="#555555",
                                  command=lambda: _thread.start_new_thread(configure, ()))
    config_button.pack(pady=20)

    load()
    root.mainloop()


if __name__ == '__main__':
    main()
