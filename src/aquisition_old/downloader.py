from pathlib import Path

def download_file(session,url,destination,chunk_size=1024*1024):
    destination=Path(destination)
    with session.get(url,stream=True,allow_redirects=True) as r:
        r.raise_for_status()
        with open(destination,'wb') as f:
            for chunk in r.iter_content(chunk_size):
                if chunk:
                    f.write(chunk)
    return destination
