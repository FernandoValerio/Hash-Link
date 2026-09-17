from urllib.parse import urlparse
def validate_url(url:str)->bool:
 p=urlparse(url); return p.scheme in ("http","https") and bool(p.netloc)
