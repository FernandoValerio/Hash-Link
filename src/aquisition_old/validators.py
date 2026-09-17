from urllib.parse import urlparse

def validate_url(url:str)->None:
    p=urlparse(url)
    if p.scheme not in {'http','https'}:
        raise ValueError('URL inválida')
    if not p.netloc:
        raise ValueError('Host inválido')
