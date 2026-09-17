from dataclasses import dataclass
@dataclass(slots=True)
class DiscoveredFile:
    name:str
    url:str
    file_id: str | None = None
    size:int|None=None
    mime_type:str|None=None
    selected: bool = True
    hash_selected: bool = True