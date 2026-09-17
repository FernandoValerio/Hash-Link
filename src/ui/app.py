from pathlib import Path

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from src.ui.main_window import MainWindow

STYLE_PATH = Path(__file__).parent / "assets" / "style.qss"
ICON_PATH = Path(__file__).parent / "assets" / "icon.ico"


def load_stylesheet() -> str:
    try:
        return STYLE_PATH.read_text(encoding="utf-8")
    except OSError:
        return ""

def main():
    app = QApplication([])
    app.setStyleSheet(load_stylesheet())
    app.setWindowIcon(QIcon(str(ICON_PATH)))
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
