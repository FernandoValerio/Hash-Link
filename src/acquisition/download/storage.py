from pathlib import Path
def ensure_output_dir(path="output"): Path(path).mkdir(exist_ok=True); return Path(path)
