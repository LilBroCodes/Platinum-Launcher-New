import requests
from typing import Dict, Any


def get_versions(branch_id=0) -> Dict[str, Any]:
    """
    Retrieve a list of versions for a given branch.

    Args:
        branch_id (int): The ID of the branch to get versions for. Defaults to 0.

    Returns:
        Dict[str, Any]: A dictionary containing the versions for the specified branch.
    """
    url = f"https://platinum.141412.xyz/launcher/api/endpoints/versions_list.php?branch_id={branch_id}"
    response = requests.get(url)
    return response.json()


def get_branches() -> Dict[str, Any]:
    """
    Retrieve a list of branches.

    Returns:
        Dict[str, Any]: A dictionary containing all branches.
    """
    url = f"https://platinum.141412.xyz/launcher/api/endpoints/branches_list.php"
    response = requests.get(url)
    return response.json()


def changelogs(branch_id=0) -> Dict[str, Any]:
    """
    Retrieve the changelog for a given branch.

    Args:
        branch_id (int): The ID of the branch to get the changelog for. Defaults to 0.

    Returns:
        Dict[str, Any]: A dictionary containing the changelog for the specified branch.
    """
    url = f"https://platinum.141412.xyz/launcher/api/endpoints/changelog.php?branch_id={branch_id}"
    response = requests.get(url)
    return response.json()


def create_branch(name: str, token: str) -> Dict[str, Any]:
    """
    Create a new branch.

    Args:
        name (str): The name of the branch to create.
        token (str): The authorization token for the request.

    Returns:
        Dict[str, Any]: A dictionary containing the response from the API after attempting to create the branch.
    """
    url = "https://platinum.141412.xyz/launcher/api/endpoints/create_branch.php"
    headers = {
        "Authorization": token
    }
    payload = {
        "branch_name": name
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()


def login(username: str, password: str) -> Dict[str, Any]:
    """
    Log in a user.

    Args:
        username (str): The username of the user.
        password (str): The password of the user.

    Returns:
        Dict[str, Any]: A dictionary containing the response from the API after attempting to log in.
    """
    url = "https://platinum.141412.xyz/launcher/api/auth/login.php"
    payload = {
        "username": username,
        "password": password
    }
    response = requests.post(url, json=payload)
    return response.json()


def download(version_id) -> Dict[str, Any]:
    """
    Download a version by its ID.

    Args:
        version_id (str): The ID of the version to download.

    Returns:
        Dict[str, Any]: A dictionary containing the response from the API after attempting to download the version.
    """
    url = f"https://platinum.141412.xyz/launcher/api/endpoints/download_version.php?version_id={version_id}"
    response = requests.get(url)
    if response.status_code != 200:
        return response.json()
    else:
        filename = response.headers.get("Content-Disposition")
        if filename:
            filename = filename.split('filename=')[1].strip('"')
        else:
            filename = "data.zip"
        return {
            "filename": filename,
            "response": response
        }


def create_version(token: str, file_path: str, branch_id: int, version_number: str, changelog: str) -> Dict[str, Any]:
    """
    Create a new version.

    Args:
        token (str): The authorization token for the request.
        file_path (str): The path to the file associated with the version.
        branch_id (int): The ID of the branch to which the version belongs.
        version_number (str): The number of the version being created.
        changelog (str): A description of the changes made in this version.

    Returns:
        Dict[str, Any]: A dictionary containing the response from the API after attempting to create the version.
    """
    url = "https://platinum.141412.xyz/launcher/api/endpoints/create_version.php"
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    data = {
        'branch_id': branch_id,
        'version_number': version_number,
        'changelog': changelog,
        'file_path': file_path
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()


def verify_versions():
    url = "https://platinum.141412.xyz/launcher/api/endpoints/verify_versions.php"
    return requests.get(url).json()
