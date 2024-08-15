import os

def rename_first_zip_in_folder(folder_path, version_tag):
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.zip'):
            original_zip_path = os.path.join(folder_path, file_name)
            new_zip_name = f"{version_tag}.zip"
            new_zip_path = os.path.join(folder_path, new_zip_name)
            os.rename(original_zip_path, new_zip_path)
            print(f"Renamed {file_name} to {new_zip_name}")
            return True
    return False

def rename_zip_files(repo):
    repo_name = repo.split('/')[-1]
    if not os.path.exists(repo_name):
        print(f"Folder '{repo_name}' does not exist.")
        return

    for version_folder in os.listdir(repo_name):
        version_folder_path = os.path.join(repo_name, version_folder)
        if os.path.isdir(version_folder_path):
            success = rename_first_zip_in_folder(version_folder_path, version_folder)
            if not success:
                print(f"No zip file found in {version_folder_path}")

if __name__ == "__main__":
    repo_name = input("Enter the GitHub repository name (e.g., 'repo_name'): ")
    rename_zip_files(repo_name)
