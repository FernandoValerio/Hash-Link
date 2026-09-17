import json
from pathlib import Path

class ManifestWriter:
    def write(self, manifest:dict, destination:str):
        path=Path(destination)
        path.write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding="utf-8")
        return path
