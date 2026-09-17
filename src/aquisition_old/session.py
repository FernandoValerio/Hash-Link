from requests import Session

def create_session()->Session:
    s=Session()
    s.headers.update({'User-Agent':'Hash-Link/0.1'})
    return s
