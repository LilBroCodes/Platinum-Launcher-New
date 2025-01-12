import os
import subprocess
import platform
from dialogue import info_popup


def universal_exec_open(filename: str, args: list[str], working_directory: str = None) -> bool or None:
    try:
        full_path = os.path.join(os.getcwd(), filename)

        if working_directory:
            working_directory = os.path.abspath(working_directory)

        print(f"#Debug | Working Directory: {working_directory}")
        print(f"#Debug | Full Path: {full_path}")

        if platform.system() == "Linux":
            try:
                subprocess.run(["wine", full_path] + args, check=True, cwd=working_directory)
            except FileNotFoundError:
                info_popup("textOnly", "Error", "Wine not found!", do_exit=False, width=200, height=150,
                           font_family="Roboto Medium", close="Ok")
                return False
        elif platform.system() == "Windows":
            subprocess.run([full_path] + args, check=True, cwd=working_directory)
        else:
            info_popup("textOnly", "Error", "Unsupported platform!", do_exit=False, width=200, height=150,
                       font_family="Roboto Medium", close="Ok")
            return False
        return True
    except subprocess.CalledProcessError as e:
        info_popup("textOnly", "Error", f"Process failed with code: {e}", do_exit=False, width=200, height=150,
                   font_family="Roboto Medium", close="Ok")
        return False
