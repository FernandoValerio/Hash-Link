from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QLabel,
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
