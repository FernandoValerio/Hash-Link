from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QLabel,
    QListWidget,
)


class HistoryPage(QWidget):
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
        title = QLabel("Aquisições anteriores")
        title.setProperty("class", "CardTitle")
        header_row.addWidget(title)
        header_row.addStretch(1)
        inner.addLayout(header_row)

        self.list_widget = QListWidget()
        self.list_widget.setObjectName("HistoryList")
        self.list_widget.setFrameShape(QFrame.NoFrame)
        inner.addWidget(self.list_widget, stretch=1)

        self.empty_state_label = QLabel(
            "Nenhuma aquisição registrada ainda.\nO histórico de URLs analisadas aparecerá aqui."
        )
        self.empty_state_label.setProperty("class", "EmptyState")
        self.empty_state_label.setAlignment(Qt.AlignCenter)
        inner.addWidget(self.empty_state_label)
        self._update_empty_state()

        self.list_widget.model().rowsInserted.connect(self._update_empty_state)
        self.list_widget.model().rowsRemoved.connect(self._update_empty_state)

        layout.addWidget(card)

    def _update_empty_state(self, *args):
        has_items = self.list_widget.count() > 0
        self.empty_state_label.setVisible(not has_items)
        self.list_widget.setVisible(has_items)
