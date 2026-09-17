from dataclasses import dataclass,field
from .discovered_file import DiscoveredFile
@dataclass(slots=True)
class AcquisitionResult:
 source_url:str
 final_url:str
 status_code:int
 content_type:str
 discovered_files:list[DiscoveredFile]=field(default_factory=list)
