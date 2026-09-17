from dataclasses import dataclass
from datetime import datetime

@dataclass(slots=True)
class ExportResult:
    export_format:str
    output_file:str
    created_at:datetime
