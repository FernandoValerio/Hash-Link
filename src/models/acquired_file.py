from dataclasses import dataclass, field
from .hash_result import HashResult

@dataclass(slots=True)
class AcquiredFile:
    name:str
    url:str
    size:int|None=None
    mime_type:str|None=None
    local_path:str|None=None
    hashes:list[HashResult]=field(default_factory=list)
