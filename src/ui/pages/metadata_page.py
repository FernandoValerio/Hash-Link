from pathlib import Path

from PIL import Image
from PIL.ExifTags import TAGS

from src.metadata.metadata_service import MetadataService

from PySide6.QtWidgets import QGridLayout
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QScrollArea,
    QFrame,
    QPushButton,
    QDialog,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)

class MetadataDialog(QDialog):

    def __init__(self, file_path: Path, parent=None):
        super().__init__(parent)

        self.setWindowTitle(
            f"Metadados - {file_path.name}"
        )

        self.resize(900, 600)

        layout = QVBoxLayout(self)

        table = QTableWidget()
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(
            ["Propriedade", "Valor"]
        )

        table.horizontalHeader().setSectionResizeMode(
            0,
            QHeaderView.ResizeToContents
        )

        table.horizontalHeader().setSectionResizeMode(
            1,
            QHeaderView.Stretch
        )

        layout.addWidget(table)

        try:

            metadata = MetadataService.extract(
                file_path
            )

            rows = list(
                metadata.full_data.items()
            )

            table.setRowCount(
                len(rows)
            )

            for row, (key, value) in enumerate(rows):

                table.setItem(
                    row,
                    0,
                    QTableWidgetItem(
                        str(key)
                    )
                )

                table.setItem(
                    row,
                    1,
                    QTableWidgetItem(
                        str(value)
                    )
                )

        except Exception as exc:

            table.setRowCount(1)

            table.setItem(
                0,
                0,
                QTableWidgetItem("Erro")
            )

            table.setItem(
                0,
                1,
                QTableWidgetItem(str(exc))
            )

class MetadataDialog_old(QDialog):

    def __init__(self, file_path: Path, parent=None):
        super().__init__(parent)

        self.setWindowTitle(f"EXIF - {file_path.name}")
        self.resize(900, 600)

        layout = QVBoxLayout(self)

        table = QTableWidget()
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(["Propriedade", "Valor"])

        table.horizontalHeader().setSectionResizeMode(
            0,
            QHeaderView.ResizeToContents
        )

        table.horizontalHeader().setSectionResizeMode(
            1,
            QHeaderView.Stretch
        )

        layout.addWidget(table)

        try:

            image = Image.open(file_path)
            exif = image.getexif()

            rows = []

            for tag_id, value in exif.items():

                rows.append(
                    (
                        TAGS.get(tag_id, str(tag_id)),
                        str(value)
                    )
                )

            table.setRowCount(len(rows))

            for row, (tag, value) in enumerate(rows):

                table.setItem(
                    row,
                    0,
                    QTableWidgetItem(tag)
                )

                table.setItem(
                    row,
                    1,
                    QTableWidgetItem(value)
                )

        except Exception as exc:

            table.setRowCount(1)

            table.setItem(
                0,
                0,
                QTableWidgetItem("Erro")
            )

            table.setItem(
                0,
                1,
                QTableWidgetItem(str(exc))
            )


class FileTile(QFrame):

    def __init__(
            self,
            file_path,
            metadata,
            callback
    ):
        super().__init__()

        self.setProperty(
            "class",
            "Card"
        )

        layout = QVBoxLayout(self)

        icon = {
            "Imagem": "📷",
            "PDF": "📄",
            "DOCX": "📝",
            "XLSX": "📊",
            "ZIP": "📦",
            "Arquivo": "📁"
        }

        emoji = icon.get(
            metadata.file_type,
            "📁"
        )

        title = QLabel(
            f"{emoji} {file_path.name}"
        )

        title.setProperty(
            "class",
            "CardTitle"
        )

        layout.addWidget(title)

        type_label = QLabel(
            f"Tipo: {metadata.file_type}"
        )

        layout.addWidget(
            type_label
        )

        for key, value in metadata.summary.items():
            label = QLabel(
                f"{key}: {value}"
            )

            layout.addWidget(
                label
            )

        button = QPushButton(
            "Ver Metadados"
        )

        button.clicked.connect(
            lambda: callback(
                file_path
            )
        )

        layout.addWidget(
            button)


class FileTile_old(QFrame):

    def __init__(self, file_path: Path, exif_summary: dict, callback):
        super().__init__()

        self.setProperty("class", "Card")

        layout = QVBoxLayout(self)

        title = QLabel(f"📷 {file_path.name}")
        title.setProperty("class", "CardTitle")

        manufacturer = QLabel(
            f"Fabricante: {exif_summary.get('make', 'N/D')}"
        )

        model = QLabel(
            f"Modelo: {exif_summary.get('model', 'N/D')}"
        )

        date = QLabel(
            f"Data: {exif_summary.get('date', 'N/D')}"
        )

        gps = QLabel(
            f"GPS: {'Sim' if exif_summary.get('gps') else 'Não'}"
        )

        size = QLabel(
            f"Dimensões: {exif_summary.get('size', 'N/D')}"
        )

        button = QPushButton(
            "Ver Metadados completos"
        )

        button.clicked.connect(
            lambda: callback(file_path)
        )

        layout.addWidget(title)
        layout.addWidget(manufacturer)
        layout.addWidget(model)
        layout.addWidget(date)
        layout.addWidget(gps)
        layout.addWidget(size)
        layout.addWidget(button)

class FileTile_old1(QFrame):

    def __init__(self, file_path: Path, callback):
        super().__init__()

        self.file_path = file_path

        self.setProperty("class", "Card")

        layout = QVBoxLayout(self)

        title = QLabel(file_path.name)
        title.setProperty("class", "CardTitle")

        button = QPushButton("Ver Metadados")
        button.clicked.connect(
            lambda: callback(file_path)
        )

        layout.addWidget(title)
        layout.addWidget(button)


class MetadataPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        title = QLabel("Metadados")
        title.setProperty("class", "CardTitle")

        layout.addWidget(title)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.container = QWidget()

        self.tiles_layout = QGridLayout(
            self.container
        )

        self.tiles_layout.setSpacing(12)

        self.card_count = 0
        # self.tiles_layout = QVBoxLayout(
        #     self.container
        # )
#        self.tiles_layout.addStretch()

        self.scroll.setWidget(
            self.container
        )

        layout.addWidget(
            self.scroll
        )

        self.files = {}

    def extract_summary(self, file_path):

        summary = {
            "make": None,
            "model": None,
            "date": None,
            "gps": False,
            "size": None
        }

        try:

            image = Image.open(file_path)

            summary["size"] = (
                f"{image.width} x {image.height}"
            )

            exif = image.getexif()

            for tag_id, value in exif.items():

                tag = TAGS.get(
                    tag_id,
                    str(tag_id)
                )

                if tag == "Make":
                    summary["make"] = str(value)

                elif tag == "Model":
                    summary["model"] = str(value)

                elif tag == "DateTime":
                    summary["date"] = str(value)

                elif tag == "GPSInfo":
                    summary["gps"] = True

        except Exception:
            pass

        return summary

    def add_file(self, path):

        path = Path(path)

        if str(path) in self.files:
            return

        metadata = MetadataService.extract(
            path
        )

        tile = FileTile(
            path,
            metadata,
            self.show_metadata
        )
        # summary = self.extract_summary(path)
        #
        # tile = FileTile(
        #     path,
        #     summary,
        #     self.show_exif
        # )
        row = self.card_count // 3
        col = self.card_count % 3

        self.tiles_layout.addWidget(
            tile,
            row,
            col
        )

        self.card_count += 1
        # self.tiles_layout.insertWidget(
        #     self.tiles_layout.count() - 1,
        #     tile
        # )

        self.files[str(path)] = path

    def add_file_old(self, path):

        path = Path(path)

        if str(path) in self.files:
            return

        self.files[str(path)] = path

        tile = FileTile(
            path,
            self.show_exif
        )

        self.tiles_layout.insertWidget(
            self.tiles_layout.count() - 1,
            tile
        )

    def show_metadata(self, path):

        dlg = MetadataDialog(
            path,
            self
        )

        dlg.exec()

    def show_exif(self, path):

        dlg = MetadataDialog(
            path,
            self
        )

        dlg.exec()