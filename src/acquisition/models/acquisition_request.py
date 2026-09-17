from dataclasses import dataclass
@dataclass(slots=True)
class AcquisitionRequest:
 url:str
 username:str|None=None
 password:str|None=None
 bearer_token:str|None=None
 timeout:int=30
