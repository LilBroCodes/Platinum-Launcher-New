import customtkinter as ctk
from tkinter import filedialog, messagebox, PhotoImage
import json
import shutil
import os
import sys

FONT_FAMILY = "Roboto Medium"


class InstallerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Platinum Launcher Installer")
        self.geometry("400x300")
        self.resizable(False, False)
        self.set_icon("data/icon.png")

        # Define variables
        self.install_dir = ctk.StringVar()
        self.additional_path = ctk.StringVar()

        # Create and pack frames
        self.frames = {
            "welcome": WelcomeFrame(self),
            "select_dir": SelectDirFrame(self),
            "specify_path": SpecifyPathFrame(self),
            "complete": CompleteFrame(self)
        }

        # Display the welcome frame initially
        self.show_frame("welcome")

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

        if not os.path.exists(install_dir):
            os.makedirs(install_dir)

        shutil.copy(self.get_resource_path("Platinum Launcher.exe"), install_dir)
        shutil.copytree(self.get_resource_path("data"), os.path.join(install_dir, "data"))

        config = {"home": additional_path}
        with open(os.path.join(install_dir, "config.json"), "w") as f:
            json.dump(config, f, indent=4)

        messagebox.showinfo("Success", "Installation complete!")
        self.quit()


class WelcomeFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        ctk.CTkLabel(self, text="Welcome to the Platinum Launcher Installer", font=(FONT_FAMILY, 16)).pack(anchor="nw", padx=10, pady=10)
        ctk.CTkButton(self, text="Next", command=lambda: self.master.show_frame("select_dir")).pack(side="bottom", anchor="se", padx=10, pady=10)


class SelectDirFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        ctk.CTkLabel(self, text="Select Installation Directory", font=(FONT_FAMILY, 14)).pack(anchor="nw", padx=10, pady=10)

        self.install_dir_entry = ctk.CTkEntry(self, textvariable=self.master.install_dir, width=300)
        self.install_dir_entry.pack(anchor="nw", padx=10, pady=5)

        self.browse_button = ctk.CTkButton(self, text="Browse", command=self.select_dir)
        self.browse_button.pack(anchor="nw", padx=10, pady=10)

        ctk.CTkButton(self, text="Next", command=lambda: self.master.show_frame("specify_path")).pack(side="bottom", anchor="se", padx=10, pady=10)
        ctk.CTkButton(self, text="Back", command=lambda: self.master.show_frame("welcome")).place(x=10, y=262)

    def select_dir(self):
        directory = filedialog.askdirectory()
        if directory:
            self.master.install_dir.set(directory)
            self.master.additional_path.set(directory)


class SpecifyPathFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        ctk.CTkLabel(self, text="Specify Additional Path", font=(FONT_FAMILY, 14)).pack(anchor="nw", padx=10, pady=10)

        self.additional_path_entry = ctk.CTkEntry(self, textvariable=self.master.additional_path, width=300)
        self.additional_path_entry.pack(anchor="nw", padx=10, pady=5)

        self.browse_button = ctk.CTkButton(self, text="Browse", command=self.select_path)
        self.browse_button.pack(anchor="nw", padx=10, pady=10)

        ctk.CTkButton(self, text="Next", command=self.master.install).pack(side="bottom", anchor="se", padx=10, pady=10)
        ctk.CTkButton(self, text="Back", command=lambda: self.master.show_frame("select_dir")).place(x=10, y=262)

    def select_path(self):
        path = filedialog.askdirectory()
        if path:
            self.master.additional_path.set(path)


class CompleteFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        ctk.CTkLabel(self, text="Installation Complete", font=(FONT_FAMILY, 16)).pack(anchor="nw", padx=10, pady=10)
        ctk.CTkButton(self, text="Finish", command=self.master.quit).pack(side="bottom", anchor="se", padx=10, pady=10)


if __name__ == "__main__":
    app = InstallerApp()
    app.mainloop()
