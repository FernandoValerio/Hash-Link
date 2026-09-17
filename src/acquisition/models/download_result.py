from dataclasses import dataclass
@dataclass(slots=True)
class DownloadResult:
 file_name:str
 local_path:str
 size:int
 content_type:str
