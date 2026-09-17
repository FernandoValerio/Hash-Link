from pathlib import Path

SRC = Path("src")

REPLACEMENTS = {
    "from acquisition.": "from src.acquisition.",
    "from hashing.": "from src.hashing.",
    "from manifest.": "from src.manifest.",
    "from exporters.": "from src.exporters.",
    "from models.": "from src.models.",
    "from services.": "from src.services.",
    "from integration.": "from src.integration.",
    "from ui.": "from src.ui.",

    "import acquisition": "import src.acquisition",
    "import hashing": "import src.hashing",
    "import manifest": "import src.manifest",
    "import exporters": "import src.exporters",
}

for file in SRC.rglob("*.py"):
    content = file.read_text(encoding="utf-8")

    original = content

    for old, new in REPLACEMENTS.items():
        content = content.replace(old, new)

    if content != original:
        file.write_text(content, encoding="utf-8")
        print(f"Atualizado: {file}")