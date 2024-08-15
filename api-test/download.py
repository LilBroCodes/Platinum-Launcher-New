import lib as api

data = api.download(29)
with open(data["filename"], "wb") as file:
    for chunk in data["response"].iter_content(chunk_size=8192):
        file.write(chunk)
