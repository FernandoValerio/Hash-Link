from pathlib import Path
from urllib.parse import urlparse


def validate_url(url: str) -> bool:
    p = urlparse(url)
    return p.scheme in ("http", "https") and bool(p.netloc)


def detect_source_type(source: str) -> str:
    """Reconhece automaticamente o tipo da origem informada pelo usuário.

    Retorna "url" (http/https), "local_file", "local_folder" ou "invalid".
    Aceita o caminho local com ou sem aspas e com o prefixo opcional
    "file://", já que é comum colar caminhos copiados do explorador de
    arquivos dessa forma.
    """
    source = (source or "").strip()
    if not source:
        return "invalid"

    if validate_url(source):
        return "url"

    candidate = source
    if candidate.lower().startswith("file://"):
        candidate = candidate[7:]
    candidate = candidate.strip('"').strip("'")

    path = Path(candidate)
    if path.is_file():
        return "local_file"
    if path.is_dir():
        return "local_folder"
    return "invalid"
