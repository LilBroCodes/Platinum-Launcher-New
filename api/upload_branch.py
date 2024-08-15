import os
import lib  # Assuming your provided library is named `lib.py`

def get_changelog(version_folder):
    changelog_path = os.path.join(version_folder, 'changelog.txt')
    if os.path.exists(changelog_path):
        with open(changelog_path, 'r', encoding='utf-8') as file:
            return file.read()
    else:
        print(f"No changelog.txt found in {version_folder}.")
        return None

def confirm(prompt):
    while True:
        user_input = input(f"{prompt} (yes/no): ").strip().lower()
        if user_input in ['yes', 'no']:
            return user_input == 'yes'

def upload_versions(repo_folder, branch_id, username, password):
    # Authenticate
    auth_response = lib.login(username, password)
    if 'token' not in auth_response:
        print("Login failed:", auth_response)
        return
    token = auth_response['token']

    # Track whether confirmation prompts have been shown
    first_upload = True
    first_response = True

    # Process each version folder
    for version_folder in os.listdir(repo_folder):
        version_folder_path = os.path.join(repo_folder, version_folder)
        if os.path.isdir(version_folder_path):
            # Find the first .zip file in the version folder
            zip_file = next((f for f in os.listdir(version_folder_path) if f.endswith('.zip')), None)
            if not zip_file:
                print(f"No .zip file found in {version_folder}. Skipping.")
                continue

            # Build the file path and changelog
            file_path = f"/data/launcher/branches/{branch_id}/{repo_folder}/{zip_file}"
            changelog = get_changelog(version_folder_path)
            if not changelog:
                continue

            # Confirm the upload details for the first version
            if first_upload:
                print(f"Ready to upload version: {version_folder}")
                print(f"File path: {file_path}")
                print(f"Changelog: {changelog}")
                if not confirm("Do you want to proceed with this upload?"):
                    print("Upload skipped.")
                    continue
                first_upload = False

            # Upload the version
            upload_response = lib.create_version(token, file_path, branch_id, version_folder, changelog)
            print("Upload response:", upload_response)

            # Confirm the server's response only for the first upload
            if first_response:
                if not confirm("Do you want to continue with the next version?"):
                    print("Upload process halted.")
                    break
                first_response = False

if __name__ == "__main__":
    repo_folder = input("Enter the path to the repository folder: ")
    branch_id = input("Enter the branch ID: ")
    username = "LilBroCodes"
    password = "Napsugar2010*"

    upload_versions(repo_folder, branch_id, username, password)
