from dataclasses import dataclass, field

@dataclass
class DiscoveredFile:
    name:str
    url:str
    size:int|None=None
    mime_type:str|None=None

@dataclass
class AcquisitionResult:
    source_url:str
    final_url:str
    status_code:int
    content_type:str
    discovered_files:list[DiscoveredFile]=field(default_factory=list)
