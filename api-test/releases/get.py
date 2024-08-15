import os
import requests
from tqdm import tqdm

def download_file(url, dest_folder):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    local_filename = os.path.join(dest_folder, url.split('/')[-1])
    with requests.get(url, stream=True) as r:
        total_length = int(r.headers.get('content-length', 0))
        with open(local_filename, 'wb') as f, tqdm(
                desc=local_filename,
                total=total_length,
                unit='iB',
                unit_scale=True,
                unit_divisor=1024,
        ) as bar:
            for chunk in r.iter_content(chunk_size=1024):
                size = f.write(chunk)
                bar.update(size)
    return local_filename

def get_releases(repo):
    url = f'https://api.github.com/repos/{repo}/releases'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def download_github_releases(repo):
    repo_name = repo.split('/')[-1]
    for release in get_releases(repo):
        version_tag = release.get('tag_name', 'unknown_version')
        assets = release.get('assets', [])
        release_folder = os.path.join(repo_name, version_tag)
        for asset in assets:
            if 'source code' not in asset['name'].lower():
                download_url = asset['browser_download_url']
                download_file(download_url, release_folder)

if __name__ == "__main__":
    repo_link = input("Enter the GitHub repository (e.g., 'owner/repo'): ")
    download_github_releases(repo_link)
