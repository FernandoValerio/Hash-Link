from pathlib import Path

def download(session,url,destination,callback=None):
    destination=Path(destination)
    with session.get(url,stream=True) as r:
        r.raise_for_status()
        total=int(r.headers.get('Content-Length',0))
        received=0
        with open(destination,'wb') as f:
            for chunk in r.iter_content(1024*1024):
                if chunk:
                    f.write(chunk)
                    received+=len(chunk)
                    if callback:
                        callback(received,total)
    return destination
