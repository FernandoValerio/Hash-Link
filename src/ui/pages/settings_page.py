from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFrame,
    QLabel,
    QCheckBox,
)


class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        layout.addWidget(self._build_security_card())
        layout.addStretch(1)

    def _build_security_card(self):
        card = QFrame()
        card.setProperty("class", "Card")
        inner = QVBoxLayout(card)
        inner.setContentsMargins(20, 16, 20, 18)
        inner.setSpacing(10)

        title = QLabel("Segurança")
        title.setProperty("class", "CardTitle")
        inner.addWidget(title)

        self.ssl_checkbox = QCheckBox("Validar certificado SSL das conexões")
        inner.addWidget(self.ssl_checkbox)
        self.ssl_checkbox.setChecked(True)

        hint = QLabel(
            "Desative apenas se precisar acessar servidores com certificados "
            "autoassinados ou inválidos."
        )
        hint.setProperty("class", "CardHint")
        hint.setWordWrap(True)
        inner.addWidget(hint)

        return card
