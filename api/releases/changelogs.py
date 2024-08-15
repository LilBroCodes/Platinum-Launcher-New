import os
import requests

def get_releases(repo):
    url = f'https://api.github.com/repos/{repo}/releases'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def save_changelog(repo, version_tag, changelog_text):
    repo_name = repo.split('/')[-1]
    version_folder = os.path.join(repo_name, version_tag)
    if not os.path.exists(version_folder):
        print(f"Folder '{version_folder}' does not exist, creating it.")
        os.makedirs(version_folder)

    changelog_path = os.path.join(version_folder, 'changelog.txt')
    with open(changelog_path, 'w', encoding='utf-8') as changelog_file:
        changelog_file.write(changelog_text)
    print(f"Saved changelog for {version_tag} to {changelog_path}")

def create_changelog_files(repo):
    repo_name = repo.split('/')[-1]
    releases = get_releases(repo)

    if not os.path.exists(repo_name):
        print(f"Main folder '{repo_name}' does not exist, creating it.")
        os.makedirs(repo_name)

    for release in releases:
        version_tag = release.get('tag_name', 'unknown_version')
        changelog_text = release.get('body', 'No description provided.')
        save_changelog(repo, version_tag, changelog_text)

if __name__ == "__main__":
    repo_link = input("Enter the GitHub repository (e.g., 'owner/repo'): ")
    create_changelog_files(repo_link)
