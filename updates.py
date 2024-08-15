import customtkinter as ctk
from tkinter import messagebox
import update_manager  # Assuming your script is named update_manager.py


class UpdateManagerGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Update Manager")
        self.geometry("300x250")

        # Branch ID input
        self.branch_label = ctk.CTkLabel(self, text="Branch ID:")
        self.branch_label.pack(pady=5)
        self.branch_entry = ctk.CTkEntry(self)
        self.branch_entry.pack(pady=5)

        # Version ID input
        self.version_label = ctk.CTkLabel(self, text="Version ID:")
        self.version_label.pack(pady=5)
        self.version_entry = ctk.CTkEntry(self)
        self.version_entry.pack(pady=5)

        # Install button
        self.install_button = ctk.CTkButton(self, text="Install", command=self.install)
        self.install_button.pack(pady=20)

    def install(self):
        branch_id = self.branch_entry.get()
        version_id = self.version_entry.get()

        if not branch_id.isdigit() or not version_id.isdigit():
            messagebox.showerror("Input Error", "Branch ID and Version ID must be numeric.")
            return

        branch_id = int(branch_id)
        version_id = int(version_id)

        try:
            update_manager.install_branch(branch_id, version_id)
            messagebox.showinfo("Success", "Installation completed successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    app = UpdateManagerGUI()
    app.mainloop()
