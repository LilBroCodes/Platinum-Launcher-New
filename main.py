from PIL import Image
import tkinter as tk
import customtkinter as ctk
from dialogue import info_popup
import api
from typing import List, Dict, Any
import update_manager


texture_pack_option_menu = None
mod_option_menu = None


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
    """
    info_popup("textOnly", "Credits", text=data, do_exit=False, width=450, height=400, font_family="Arial")


def version_selector(data: List[Dict[str, Any]], root: ctk.ctk_tk, w: int, h: int, placeholder: str):
    dnames = [version["version_number"] for version in data]
    dnames.insert(0, placeholder)
    return ctk.CTkOptionMenu(root, width=w, height=h, values=dnames, fg_color="#333333",
                             dropdown_fg_color="#333333", dropdown_hover_color="#595959", button_color="#333333",
                             button_hover_color="#595959", corner_radius=5)


def mod_selector(root: ctk.ctk_tk, w: int, h: int):
    mod_options = ["None", "PolzHax", "Mat's Nice Hacks"]
    return ctk.CTkOptionMenu(root, width=w, height=h, values=mod_options, fg_color="#333333",
                             dropdown_fg_color="#333333", dropdown_hover_color="#595959", button_color="#333333",
                             button_hover_color="#595959", corner_radius=5)


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
                             button_hover_color="#595959", corner_radius=5)


def download_version(version):
    game_versions = api.get_versions(2)
    version_data = [idx for idx in game_versions if idx["version_number"] == version]
    id = version_data[0]["id"]
    update_manager.install_branch(2, 30)
    mod_option_menu.configure(state="normal")
    texture_pack_option_menu.configure(state="normal")


def configure_mod(mod):
    print(mod)


def configure_texture_pack(texture_pack):
    print(f"Configuring texture pack: {texture_pack}")


def main():
    root = ctk.CTk()
    root.title("Platinum GDPS Launcher")
    root.geometry("1000x750")
    root.iconbitmap("data/favicon.ico")
    img = tk.PhotoImage(file="data/icon.png")
    root.tk.call('wm', 'iconphoto', root._w, img)

    font_family = "Arial"

    bottom_frame = ctk.CTkFrame(root, height=50, bg_color="#333333", border_width=0)
    bottom_frame.pack(side="bottom", fill="x")

    top_frame = ctk.CTkFrame(root, height=50, bg_color="#333333", border_width=0)
    top_frame.pack(side="top", fill="x")

    text_label = ctk.CTkLabel(bottom_frame, text="Made by LilBroCodes & Zud", font=(font_family, 16),
                              text_color="#909090")
    text_label.pack(side="left", padx=10, pady=10)

    version_label = ctk.CTkLabel(bottom_frame, text="Platinum GDPS Launcher pre-01", font=(font_family, 16),
                                 text_color="#909090")
    version_label.pack(side="right", padx=10, pady=10)

    launch_button = ctk.CTkButton(top_frame, text="Launch", font=(font_family, 20), text_color="white", fg_color="#444444",
                                  hover_color="#555555", width=120, height=50)
    launch_button.pack(side="right", padx=5)

    main_frame = ctk.CTkFrame(master=root, width=1920, height=1080, fg_color="#333333")
    main_frame.pack(side="left", padx=10, pady=10)

    image_path = "data/icon.png"
    plaster_image = ctk.CTkImage(Image.open(image_path), size=(50, 50))
    plaster = ctk.CTkButton(master=top_frame, text="", image=plaster_image, bg_color="#333333", fg_color="#333333",
                            border_color="#333333", hover_color="#333333", width=50)
    plaster.pack(padx=10, side="left")

    credits_button = ctk.CTkButton(top_frame, text="Credits", font=(font_family, 20), text_color="white", fg_color="#444444",
                                  hover_color="#555555", width=50, height=50, command=creds)
    credits_button.pack(side="left", padx=5)

    download_version_button = ctk.CTkButton(main_frame, text="Download Version", font=(font_family, 16), text_color="white",
                                           fg_color="#444444", hover_color="#555555", command=lambda: download_version(version_option_menu.get()))
    download_version_button.pack(pady=20)

    version_option_menu = version_selector(api.get_versions(2), main_frame, 300, 40, "Select Version")
    version_option_menu.pack(pady=10)

    global mod_option_menu
    global texture_pack_option_menu

    mod_option_menu = mod_selector(main_frame, 300, 40)
    mod_option_menu.pack(pady=10)
    mod_option_menu.configure(state="disabled")

    tp_data = api.get_versions(5)
    texture_pack_option_menu = texture_pack_selector(main_frame, 300, 40, data=tp_data)
    texture_pack_option_menu.pack(pady=10)
    texture_pack_option_menu.configure(state="disabled")

    def on_mod_selected(event):
        mod = mod_option_menu.get()
        configure_mod(mod)

    def on_texture_pack_selected(event):
        texture_pack = texture_pack_option_menu.get()
        configure_texture_pack(texture_pack)

    mod_option_menu.bind("<<ComboboxSelected>>", on_mod_selected)
    texture_pack_option_menu.bind("<<ComboboxSelected>>", on_texture_pack_selected)

    root.mainloop()


if __name__ == '__main__':
    main()
