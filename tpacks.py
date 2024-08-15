from PIL import Image
from dialogue import *
import api as api
from typing import List, Dict, Any


def creds():
    data = """
        Songs:
            Flourish (Platinum Pack Menu Theme) - Purrple Cat

        Images:
            Main icon - Zud
            Custom BG (Ingame, Platinum Pack) - Zud
            T̶o̶o̶l̶s̶ ̶p̶a̶g̶e̶ ̶i̶c̶o̶n̶ (Unused in current version)
            D̶e̶m̶o̶n̶l̶i̶s̶t̶ ̶i̶c̶o̶n̶ (Unused in current version)
            M̶a̶i̶n̶ ̶p̶l̶a̶s̶t̶e̶r̶ ̶i̶c̶o̶n̶ (Unused in current version)

        Mods:
            PolzHax - Pololak (https://github.com/Pololoak)
            Mat's nice hacks - matcool (https://github.com/matcool)
            
        Misc:
            Poggers hosting service - Jean
    """
    info_popup("textOnly", "Credits", text=data, do_exit=False, width=450, height=400, font_family="Arial")


def versions_selector(data: List[Dict[str, Any]], root: ctk.ctk_tk, w: int, h: int, placeholder: str):
    dnames = []
    for version in data:
        version: dict
        if version.get("display_name"):
            dnames.append(version["display_name"])
        else:
            dnames.append(version["version_number"])

    dnames.insert(0, placeholder)
    return ctk.CTkOptionMenu(root, width=w, height=h, values=dnames, fg_color="#333333",
                             dropdown_fg_color="#333333", dropdown_hover_color="#595959", button_color="#333333",
                             button_hover_color="#595959", corner_radius=5)


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

    # login_button = ctk.CTkButton(top_frame, text="Log In", font=("Arial", 13), text_color="white", fg_color="#444444",
    #                           hover_color="#555555", width=65, command=login)
    # login_button.pack(side="left", padx=5)

    # register_button = ctk.CTkButton(top_frame, text="Register", font=("Arial", 13), text_color="white",
    #                              fg_color="#444444", hover_color="#555555", width=65, command=register)
    # register_button.pack(side="left", padx=5)

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

    launch_button = ctk.CTkButton(top_frame, text="Credits", font=(font_family, 20), text_color="white", fg_color="#444444",
                                  hover_color="#555555", width=50, height=50, command=creds)
    launch_button.pack(side="left", padx=5)

    tp_data = api.get_versions(5)
    game_data = api.get_versions(2)
    polz_data = api.get_versions(1)
    mats_data = api.get_versions(3)
    # These are the data that can be used for version selecting

    root.mainloop()


if __name__ == '__main__':
    main()