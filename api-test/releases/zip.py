import os
import zipfile

def zip_files_in_folder(folder_path, zip_name):
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)

def zip_github_releases(repo):
    repo_name = repo.split('/')[-1]
    if not os.path.exists(repo_name):
        print(f"Folder '{repo_name}' does not exist.")
        return

    for version_folder in os.listdir(repo_name):
        version_folder_path = os.path.join(repo_name, version_folder)
        if os.path.isdir(version_folder_path):
            zip_name = os.path.join(repo_name, f"{version_folder}.zip")
            zip_files_in_folder(version_folder_path, zip_name)
            print(f"Zipped {version_folder} into {zip_name}")

if __name__ == "__main__":
    repo_name = input("Enter the GitHub repository name (e.g., 'repo_name'): ")
    zip_github_releases(repo_name)
