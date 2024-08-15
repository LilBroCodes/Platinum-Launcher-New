import requests
import lib as api
import json

while True:
    branch_id = int(input("Enter Branch ID: "))
    data = api.get_versions(branch_id)
    print(json.dumps(data, indent=1))
    with open(f"data-{branch_id}.json", "w") as file:
        json.dump(data, file, indent=1)
