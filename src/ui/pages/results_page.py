from PySide6.QtCore import Qt, QMimeData
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
)

class ResultsPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        card = QFrame()
        card.setProperty("class", "Card")
        inner = QVBoxLayout(card)
        inner.setContentsMargins(20, 16, 20, 16)
        inner.setSpacing(10)

        header_row = QHBoxLayout()
        title = QLabel("Hashes calculados")
        title.setProperty("class", "CardTitle")
        header_row.addWidget(title)
        header_row.addStretch(2)

        self.count_badge = QLabel("0 registros")
        self.count_badge.setProperty("class", "CountBadge")
        header_row.addWidget(self.count_badge)

        self.copy_button = QPushButton("📋  Copiar tabela")
        self.copy_button.setObjectName("SecondaryButton")
        self.copy_button.setCursor(Qt.PointingHandCursor)
        self.copy_button.clicked.connect(self.copy_table_to_clipboard)
        header_row.addWidget(self.copy_button)

        self.copy_word = QPushButton("📋  Copiar Word")
        self.copy_word.setObjectName("SecondaryButton")
        self.copy_word.setCursor(Qt.PointingHandCursor)
        self.copy_word.clicked.connect(self.copy_table_to_word)
        header_row.addWidget(self.copy_word)


        inner.addLayout(header_row)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Arquivo", "Hash MD5", "Hash SHA-256"])
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setShowGrid(False)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        inner.addWidget(self.table, stretch=1)

        self.empty_state_label = QLabel(
            "Nenhum resultado ainda.\nOs hashes calculados na aba Aquisição aparecerão aqui."
        )
        self.empty_state_label.setProperty("class", "EmptyState")
        self.empty_state_label.setAlignment(Qt.AlignCenter)
        inner.addWidget(self.empty_state_label)
        self._update_empty_state()

        layout.addWidget(card)

    def add_result(
            self,
            file_name,
            algorithm,
            hash_value,
    ):
        row = self.table.rowCount()

        self.table.insertRow(row)

        self.table.setItem(
            row,
            0,
            QTableWidgetItem(file_name)
        )

        self.table.setItem(
            row,
            1,
            QTableWidgetItem(algorithm)
        )

        self.table.setItem(
            row,
            2,
            QTableWidgetItem(hash_value)
        )

        self._update_empty_state()

    def _update_empty_state(self):
        count = self.table.rowCount()
        self.count_badge.setText(
            f"{count} registro" if count == 1 else f"{count} registros"
        )
        self.empty_state_label.setVisible(count == 0)
        self.table.setVisible(count > 0)
        self.copy_button.setEnabled(count > 0)

    def copy_table_to_word(self):
        rows = self.table.rowCount()
        cols = self.table.columnCount()
        width=["width:200px","width:230px;white-space:nowrap","width:470px"]

        if rows == 0:
            return
        html = """
        <table
            border="2"
            cellspacing="0"
            cellpadding="4"
            style="
                border-collapse:collapse;
                font-family:Calibri;
                font-size:10pt;
                width:100%;
                table-layout:fixed;
            "
        >
        """
#         html = """
#         <table style="
#             border-collapse:collapse;
#             font-family:Calibri;
#             font-size:11pt;
#         ">
#         """
#         html += "<table border='3' cellspacing='0' cellpadding='4'>"
        # Cabeçalho
        html += "<tr>"
        for c in range(cols):
            header = self.table.horizontalHeaderItem(c)
            text = header.text() if header else ""
            text = text.upper()
            html += (
                f"<th style='background:#5B5B5B;"
                f"color:#FFFFFF;"
                f"font-weight:bold;"
                f"text - align: center;"
                f"vertical - align: middle;"
                f"height:2em;"
                f"border:2px solid #000;"
                f"padding:5px;"
                f"{width[c]}'>"
                f"{text}</th>"
            )
        html += "</tr>"

    # Dados
        for r in range(rows):
            html += "<tr>"
            for c in range(cols):
                item = self.table.item(r, c)
                text = item.text() if item else ""

                html += (
                    f"<td style='"
                    f"{width[c]};"
                    f"border:2px solid black;"
                    f"padding:4px;"
                    f"{'white-space:nowrap;' if c == 1 else ''}"
                    f"'>"
#                 html += (f"<table style ="
#                          f"border:1px solid black;"
#                          f"cellpadding='2';"
# #                         f"padding:2px;"
# #                         f"border-collapse:collapse;"
#                          f" margin:'1';>"
                    f"{text}"
                       )
                html+="</td>"

 #               html += f"<td>{text}</td>"
            html += "</tr>"

        html += "</table>"

        mime = QMimeData()
        mime.setHtml(html)

        QGuiApplication.clipboard().setMimeData(mime)


    def copy_table_to_clipboard(self):
        """Copia a tabela de hashes (cabeçalho + linhas, separados por TAB) para a
        área de transferência — cola direto como tabela no Excel/Sheets ou como
        texto alinhado em qualquer editor."""
        rows = self.table.rowCount()
        cols = self.table.columnCount()
        if rows == 0:
            return

        headers = [
            self.table.horizontalHeaderItem(c).text() if self.table.horizontalHeaderItem(c) else ""
            for c in range(cols)
        ]
        lines = ["\t".join(headers)]

        for r in range(rows):
            cells = [
                self.table.item(r, c).text() if self.table.item(r, c) else ""
                for c in range(cols)
            ]
            lines.append("\t".join(cells))

        QGuiApplication.clipboard().setText("\n".join(lines))

class ResultsPage_old(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        card = QFrame()
        card.setProperty("class", "Card")
        inner = QVBoxLayout(card)
        inner.setContentsMargins(20, 16, 20, 16)
        inner.setSpacing(10)

        header_row = QHBoxLayout()
        title = QLabel("Hashes calculados")
        title.setProperty("class", "CardTitle")
        header_row.addWidget(title)
        header_row.addStretch(1)

        self.count_badge = QLabel("0 registros")
        self.count_badge.setProperty("class", "CountBadge")
        header_row.addWidget(self.count_badge)
        inner.addLayout(header_row)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Arquivo", "Algoritmo", "Hash"])
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setShowGrid(False)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        inner.addWidget(self.table, stretch=1)

        self.empty_state_label = QLabel(
            "Nenhum resultado ainda.\nOs hashes calculados na aba Aquisição aparecerão aqui."
        )
        self.empty_state_label.setProperty("class", "EmptyState")
        self.empty_state_label.setAlignment(Qt.AlignCenter)
        inner.addWidget(self.empty_state_label)
        self._update_empty_state()

        layout.addWidget(card)

    def add_result(
            self,
            file_name,
            algorithm,
            hash_value,
    ):
        row = self.table.rowCount()

        self.table.insertRow(row)

        self.table.setItem(
            row,
            0,
            QTableWidgetItem(file_name)
        )

        self.table.setItem(
            row,
            1,
            QTableWidgetItem(algorithm)
        )

        self.table.setItem(
            row,
            2,
            QTableWidgetItem(hash_value)
        )

        self._update_empty_state()

    def _update_empty_state(self):
        count = self.table.rowCount()
        self.count_badge.setText(
            f"{count} registro" if count == 1 else f"{count} registros"
        )
        self.empty_state_label.setVisible(count == 0)
        self.table.setVisible(count > 0)
