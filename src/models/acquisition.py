from dataclasses import dataclass, field
from datetime import datetime

@dataclass(slots=True)
class Acquisition:
    acquisition_id:str
    source_url:str
    final_url:str
    started_at:datetime
    finished_at:datetime|None=None
    status:str="pending"
    algorithms:list[str]=field(default_factory=list)
