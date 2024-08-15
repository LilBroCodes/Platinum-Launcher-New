import os
import shutil

def export_repo_to_data(repo_folder, branch_id):
    # Ensure the base directory exists
    base_data_path = os.path.expanduser(f"./data/launcher/branches/{branch_id}/{repo_folder}")
    if not os.path.exists(base_data_path):
        os.makedirs(base_data_path)
        print(f"Created base directory: {base_data_path}")

    # Process each version folder
    for version_folder in os.listdir(repo_folder):
        version_folder_path = os.path.join(repo_folder, version_folder)
        if os.path.isdir(version_folder_path):
            # Find the first .zip file in the version folder
            zip_file = next((f for f in os.listdir(version_folder_path) if f.endswith('.zip')), None)
            if not zip_file:
                print(f"No .zip file found in {version_folder}. Skipping.")
                continue

            source_zip_path = os.path.join(version_folder_path, zip_file)
            destination_zip_path = os.path.join(base_data_path, zip_file)

            # Copy the zip file to the base directory
            shutil.copy2(source_zip_path, destination_zip_path)
            print(f"Copied {source_zip_path} to {destination_zip_path}")

if __name__ == "__main__":
    repo_folder = input("Enter the path to the repository folder: ")
    branch_id = input("Enter the branch ID: ")

    export_repo_to_data(repo_folder, branch_id)
