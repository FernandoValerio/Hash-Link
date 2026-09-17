from dataclasses import dataclass, field
from .acquired_file import AcquiredFile

@dataclass(slots=True)
class Manifest:
    acquisition_id:str
    source_url:str
    final_url:str
    started_at:str
    finished_at:str
    algorithms:list[str]=field(default_factory=list)
    files:list[AcquiredFile]=field(default_factory=list)
