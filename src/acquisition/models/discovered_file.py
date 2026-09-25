from dataclasses import dataclass
@dataclass(slots=True)
class DiscoveredFile:
    name:str
    url:str=""
    file_id: str | None = None
    size:int|None=None
    mime_type:str|None=None
    selected: bool = True
    hash_selected: bool = True
    # Arquivo de origem local (em vez de um link a ser baixado). Quando
    # is_local=True, `local_path` traz o caminho no disco e `url` fica vazio
    # — o download HTTP é pulado e o arquivo é copiado/lido direto dali.
    is_local: bool = False
    local_path: str | None = None