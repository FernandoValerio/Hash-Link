from dataclasses import dataclass
from datetime import datetime

@dataclass(slots=True)
class HashResult:
    algorithm:str
    value:str
    calculated_at:datetime
