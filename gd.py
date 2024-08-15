import os
import subprocess


def universal_exec_open(filename: str, args: list[str], working_directory: str = None) -> bool or None:
    try:
        full_path = os.path.join(os.getcwd(), filename)

        if working_directory:
            working_directory = os.path.abspath(working_directory)

        print(f"#Debug | Working Directory: {working_directory}")
        print(f"#Debug | Full Path: {full_path}")

        subprocess.run([full_path] + args, check=True, cwd=working_directory)
        return True
    except subprocess.CalledProcessError as e:
        if "returned non-zero exit status 1." not in str(e):
            raise RuntimeError(f"Process failed with code: {e}")
