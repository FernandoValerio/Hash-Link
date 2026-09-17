from dataclasses import dataclass, field
from typing import Optional

@dataclass(slots=True)
class DiscoveredFile:
    name:str
    url:str
    size:Optional[int]=None
    mime_type:Optional[str]=None

@dataclass(slots=True)
class AcquisitionRequest:
    url:str
    username:str|None=None
    password:str|None=None

@dataclass(slots=True)
class AcquisitionResult:
    source_url:str
    final_url:str
    status_code:int
    content_type:str
    discovered_files:list[DiscoveredFile]=field(default_factory=list)
