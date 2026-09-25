from pathlib import Path
import sys


def resource_path(relative_path: str) -> Path:

    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / relative_path

    return Path(__file__).parent / relative_path