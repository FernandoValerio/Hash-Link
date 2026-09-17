import json
from pathlib import Path

def write_manifest(data:dict,path:str):
    p=Path(path)
    p.write_text(json.dumps(data,indent=2),encoding='utf-8')
    return p
