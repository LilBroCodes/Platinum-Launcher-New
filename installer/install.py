import customtkinter as ctk
from tkinter import filedialog, messagebox, PhotoImage, Scrollbar, VERTICAL
import json
import shutil
import os
import sys

from dialogue import check_case_insensitive, info_popup

FONT_FAMILY = "Roboto Medium"


class InstallerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Platinum Launcher Installer")
        self.geometry("800x600")
        self.resizable(False, False)
        self.set_icon("data/icon.png")

        # Define variables
        self.install_dir = ctk.StringVar()
        self.additional_path = ctk.StringVar()
        self.create_desktop_shortcut = ctk.BooleanVar(value=True)

        # Create and pack frames
        self.frames = {
            "license": LicenseFrame(self),
            "select_dir": SelectDirFrame(self),
            "specify_path": SpecifyPathFrame(self),
            "shortcut_options": ShortcutOptionsFrame(self),
            "complete": CompleteFrame(self)
        }

        # Display the license frame initially
        self.show_frame("license")

    def get_resource_path(self, relative_path):
        """Get the absolute path to a resource, relative to the executable or script."""
        if getattr(sys, 'frozen', False):
            # If the application is frozen, use the temp directory
            base_path = sys._MEIPASS
        else:
            # If the application is running in a normal Python environment
            base_path = os.path.dirname(__file__)
        return os.path.join(base_path, relative_path)

    def set_icon(self, icon_path):
        """Set the window icon."""
        icon_path = self.get_resource_path(icon_path)
        if os.path.isfile(icon_path):
            self.iconbitmap(icon_path)
            img = PhotoImage(file=icon_path)
            self.tk.call('wm', 'iconphoto', self._w, img)
        else:
            print(f"Icon file not found: {icon_path}")

    def show_frame(self, page_name):
        # Hide all frames
        for frame in self.frames.values():
            frame.pack_forget()

        # Show the requested frame
        frame = self.frames[page_name]
        frame.pack(fill="both", expand=True)
        frame.tkraise()

    def install(self):
        install_dir = self.install_dir.get()
        additional_path = self.additional_path.get()

        if not install_dir:
            messagebox.showerror("Error", "Please select an installation directory.")
            return

        if os.path.exists(install_dir):
            if os.listdir(install_dir):
                messagebox.showerror("Error", "The selected installation directory is not empty. Please select an "
                                              "empty directory.")
                return
        else:
            os.makedirs(install_dir)

        shutil.copy(self.get_resource_path("Platinum Launcher.exe"), install_dir)
        shutil.copytree(self.get_resource_path("data"), os.path.join(install_dir, "data"))

        config = {"home": additional_path}
        with open(os.path.join(install_dir, "config.json"), "w") as f:
            json.dump(config, f, indent=4)

        if self.create_desktop_shortcut.get():
            self.create_shortcut(install_dir, "desktop")

        info_popup("textOnly", "Success", "Installation complete!", code=0, font_family=FONT_FAMILY, height=150, do_exit=True)
        self.quit()

    def create_shortcut(self, install_dir, location):
        shortcut_name = "Platinum Launcher.lnk"
        target = os.path.join(install_dir, "Platinum Launcher.exe")
        shortcut_path = os.path.join(os.path.join(os.environ["USERPROFILE"], "Desktop"), shortcut_name)

        # Using winshell to create shortcuts
        import winshell
        with winshell.shortcut(shortcut_path) as link:
            link.path = target
            link.working_directory = install_dir
            link.description = "Shortcut for Platinum Launcher"


class LicenseFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        ctk.CTkLabel(self, text="License Agreement", font=(FONT_FAMILY, 16)).pack(anchor="nw", padx=10, pady=10)

        # Create a frame to contain the textbox and scrollbar
        text_frame = ctk.CTkFrame(self)
        text_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Create the scrollable text box
        self.license_textbox = ctk.CTkTextbox(text_frame, wrap="word", font=(FONT_FAMILY, 12), height=100)
        self.license_textbox.pack(side="left", fill="both", expand=True)

        # Insert the license text into the text box
        try:
            with open(self.master.get_resource_path("license.txt"), "r") as file:
                license_text = file.read()
        except Exception as e:
            license_text = str(e)
        self.license_textbox.insert("1.0", license_text)
        self.license_textbox.configure(state="disabled")  # Make the textbox read-only

        # Accept and Decline buttons
        self.accept_button = ctk.CTkButton(self, fg_color="#444444", hover_color="#555555", text="Accept", command=self.accept_license)
        self.accept_button.pack(side="right", anchor="se", padx=10, pady=10)

        self.decline_button = ctk.CTkButton(self, fg_color="#444444", hover_color="#555555", text="Decline", command=self.decline_license)
        self.decline_button.pack(side="right", anchor="se", padx=10, pady=10)

    def accept_license(self):
        self.master.show_frame("select_dir")

    def decline_license(self):
        self.master.quit()


class SelectDirFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        c = ctk.CTkLabel(self, text="Select Launcher Installation Directory", font=(FONT_FAMILY, 14))
        c.pack(anchor="nw", padx=10, pady=10)

        self.install_dir_entry = ctk.CTkEntry(self, textvariable=self.master.install_dir, width=300)
        self.install_dir_entry.pack(anchor="nw", padx=10, pady=5)

        self.browse_button = ctk.CTkButton(self, fg_color="#444444", hover_color="#555555", text="Browse",
                                           command=self.select_dir)
        self.browse_button.pack(anchor="nw", padx=10, pady=10)

        ctk.CTkButton(self, fg_color="#444444", hover_color="#555555", text="Next",
                      command=lambda: self.master.show_frame("specify_path")).pack(side="right", anchor="se", padx=10, pady=10)
        ctk.CTkButton(self, fg_color="#444444", hover_color="#555555", text="Back",
                      command=lambda: self.master.show_frame("license")).pack(side="right", anchor="se", padx=10, pady=10)

    def select_dir(self):
        directory = filedialog.askdirectory()
        if directory:
            self.master.install_dir.set(directory)
            self.master.additional_path.set(directory + "/game")


class SpecifyPathFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        ctk.CTkLabel(self, text="Select GDPS installation directory", font=(FONT_FAMILY, 14)).pack(anchor="nw", padx=10,
                                                                                                   pady=10)

        self.additional_path_entry = ctk.CTkEntry(self, textvariable=self.master.additional_path, width=300)
        self.additional_path_entry.pack(anchor="nw", padx=10, pady=5)

        self.browse_button = ctk.CTkButton(self, fg_color="#444444", hover_color="#555555", text="Browse",
                                           command=self.select_path)
        self.browse_button.pack(anchor="nw", padx=10, pady=10)

        ctk.CTkButton(self, fg_color="#444444", hover_color="#555555", text="Next",
                      command=lambda: self.master.show_frame("shortcut_options")).pack(side="right", anchor="se", padx=10, pady=10)
        ctk.CTkButton(self, fg_color="#444444", hover_color="#555555", text="Back",
                      command=lambda: self.master.show_frame("select_dir")).pack(side="right", anchor="se", padx=10, pady=10)

    def select_path(self):
        path = filedialog.askdirectory()
        if path:
            self.master.additional_path.set(path)


class ShortcutOptionsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        ctk.CTkLabel(self, text="Create Shortcuts", font=(FONT_FAMILY, 14)).pack(anchor="nw", padx=10, pady=10)
        self.desktop_checkbox = ctk.CTkCheckBox(self, text="Create Desktop shortcut",
                                                variable=self.master.create_desktop_shortcut)
        self.desktop_checkbox.pack(anchor="nw", padx=10, pady=5)

        ctk.CTkButton(self, fg_color="#444444", hover_color="#555555", text="Install",
                      command=self.master.install).pack(side="right", anchor="se", padx=10, pady=10)
        ctk.CTkButton(self, fg_color="#444444", hover_color="#555555", text="Back",
                      command=lambda: self.master.show_frame("specify_path")).pack(side="right", anchor="se", padx=10, pady=10)


class CompleteFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        ctk.CTkLabel(self, text="Installation Complete", font=(FONT_FAMILY, 16)).pack(anchor="nw", padx=10, pady=10)
        ctk.CTkButton(self, fg_color="#444444", hover_color="#555555", text="Finish", command=self.master.quit).pack(
            side="bottom", anchor="se", padx=10, pady=10)


if __name__ == "__main__":
    app = InstallerApp()
    app.mainloop()
