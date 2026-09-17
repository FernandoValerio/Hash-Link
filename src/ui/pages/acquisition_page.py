from requests import Session
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QCheckBox,
    QRadioButton,
    QTableWidgetItem,
    QProgressBar,
    QHeaderView,
    QSizePolicy,
)

from src.services.workflow_service import WorkflowService
from src.acquisition.services.acquisition_service import AcquisitionService
from src.acquisition.download.downloader import Downloader
from src.hashing.hasher import calculate_hash

OUTPUT = r'E:\Projetos\hash_link\output'
HASH = r'E:\Projetos\hash_link\output\hash'


def _card() -> QFrame:
    card = QFrame()
    card.setProperty("class", "Card")
    return card


class AcquisitionPage(QWidget):
    def __init__(self, results_page):
        super().__init__()
        self.results_page = results_page

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        layout.addWidget(self._build_source_card())
        layout.addWidget(self._build_files_card(), stretch=1)
        layout.addWidget(self._build_actions_card())

        self.current_result = None

        self.workflow = WorkflowService(
            acquisition_service=None,
            hashing=None,
            manifest=None,
            exports=None,
        )

        self.analyse.clicked.connect(self.analyse_url)
        self.download_button.clicked.connect(self.download_selected)
        self.hash_button.clicked.connect(self.hash_selected)

    # ------------------------------------------------------------------
    # Construção da interface
    # ------------------------------------------------------------------
    def _build_source_card(self):
        card = _card()
        inner = QVBoxLayout(card)
        inner.setContentsMargins(20, 16, 20, 18)
        inner.setSpacing(10)

        title = QLabel("Origem")
        title.setProperty("class", "CardTitle")
        inner.addWidget(title)

        hint = QLabel("Informe a URL a ser analisada para descobrir os arquivos disponíveis.")
        hint.setProperty("class", "CardHint")
        inner.addWidget(hint)

        row = QHBoxLayout()
        row.setSpacing(10)

        self.url = QLineEdit()
        self.url.setPlaceholderText("https://...")
        self.url.setMinimumHeight(38)
        row.addWidget(self.url, stretch=1)

        self.analyse = QPushButton("🔍  Analisar URL")
        self.analyse.setObjectName("PrimaryButton")
        self.analyse.setMinimumHeight(38)
        self.analyse.setCursor(Qt.PointingHandCursor)
        row.addWidget(self.analyse)

        inner.addLayout(row)
        return card

    def _build_files_card(self):
        card = _card()
        inner = QVBoxLayout(card)
        inner.setContentsMargins(20, 16, 20, 16)
        inner.setSpacing(10)

        header_row = QHBoxLayout()
        title = QLabel("Arquivos encontrados")
        title.setProperty("class", "CardTitle")
        header_row.addWidget(title)
        header_row.addStretch(1)

        self.files_count_badge = QLabel("0 arquivos")
        self.files_count_badge.setProperty("class", "CountBadge")
        header_row.addWidget(self.files_count_badge)
        inner.addLayout(header_row)

        self.output = QTableWidget()
        self.output.setColumnCount(3)
        self.output.setHorizontalHeaderLabels(["Nome", "Download", "Hash"])
        self.output.verticalHeader().setVisible(False)
        self.output.setAlternatingRowColors(True)
        self.output.setSelectionBehavior(QTableWidget.SelectRows)
        self.output.setEditTriggers(QTableWidget.NoEditTriggers)
        self.output.setShowGrid(False)
        header = self.output.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        inner.addWidget(self.output, stretch=1)

        self.empty_state_label = QLabel(
            "Nenhum arquivo listado ainda.\nInforme uma URL acima e clique em “Analisar URL”."
        )
        self.empty_state_label.setProperty("class", "EmptyState")
        self.empty_state_label.setAlignment(Qt.AlignCenter)
        inner.addWidget(self.empty_state_label)
        self._update_empty_state(True)

        return card

    def _build_actions_card(self):
        card = _card()
        inner = QVBoxLayout(card)
        inner.setContentsMargins(20, 16, 20, 18)
        inner.setSpacing(10)

        row = QHBoxLayout()
        row.setSpacing(10)

        self.download_button = QPushButton("⬇️  Baixar Selecionados")
        self.download_button.setObjectName("SecondaryButton")
        self.download_button.setCursor(Qt.PointingHandCursor)
        row.addWidget(self.download_button)

        self.hash_button = QPushButton("🧬  Hash Selecionados")
        self.hash_button.setObjectName("PrimaryButton")
        self.hash_button.setCursor(Qt.PointingHandCursor)
        row.addWidget(self.hash_button)

        row.addStretch(1)
        inner.addLayout(row)

        progress_label = QLabel("Progresso")
        progress_label.setProperty("class", "CardHint")
        inner.addWidget(progress_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        inner.addWidget(self.progress_bar)

        return card

    def _update_empty_state(self, is_empty: bool):
        self.empty_state_label.setVisible(is_empty)
        self.output.setVisible(not is_empty)

    # ------------------------------------------------------------------
    # Lógica (inalterada em relação à versão original)
    # ------------------------------------------------------------------
    def analyse_url(self):
        url = self.url.text().strip()

        try:
            service = AcquisitionService()

            result = service.analyse(url)

            self.output.setRowCount(len(result.discovered_files))

            for row, file in enumerate(result.discovered_files):
                download_check = QCheckBox()
                hash_check = QCheckBox()

                download_check.setChecked(True)
                hash_check.setChecked(True)

                self.output.setItem(row, 0, QTableWidgetItem(file.name))
                self.output.setCellWidget(row, 1, download_check)
                self.output.setCellWidget(row, 2, hash_check)

            self.current_result = result

            count = len(result.discovered_files)
            self.files_count_badge.setText(
                f"{count} arquivo" if count == 1 else f"{count} arquivos"
            )
            self._update_empty_state(count == 0)

        except Exception as exc:
            self.current_result = None
            self.output.setRowCount(0)
            self.files_count_badge.setText("0 arquivos")
            self.empty_state_label.setText(f"Erro:\n{exc}")
            self._update_empty_state(True)

    def download_selected(self):

        if self.current_result is None:
            return

        selected_files = []

        for row, file in enumerate(
                self.current_result.discovered_files
        ):

            checkbox = self.output.cellWidget(
                row,
                1
            )

            if checkbox.isChecked():
                selected_files.append(file)
        session = Session()
        downloader = Downloader()
        for file in selected_files:
            self.progress_bar.setValue(0)
            destination = f'{OUTPUT}\\{file.name}'
            downloader.download(session=session, url=file.url, destination=destination, callback=self.progress)
            print(f'baixado: {file.name}')

    def progress(self, got, total):

        if total > 0:
            percent = (
                              got / total
                      ) * 100

            self.progress_bar.setValue(percent)

    def hash_selected(self):

        selected_files = []

        for row, file in enumerate(
                self.current_result.discovered_files
        ):

            checkbox = self.output.cellWidget(
                row,
                2
            )

            if checkbox.isChecked():
                selected_files.append(
                    file
                )
        session = Session()
        downloader = Downloader()
        hash_tipe = "SHA-256"
        for file in selected_files:
            destination = f'{HASH}\\{file.name}'
            downloader.download(session=session, url=file.url, destination=destination, callback=self.progress)
        for file in selected_files:
            local_file = (
                Path(f'{HASH}\\{file.name}'))

            if not local_file.exists():
                continue

            hash_value = calculate_hash(local_file, hash_tipe)
            self.results_page.add_result(
                file.name,
                hash_tipe,
                hash_value
            )

        print(selected_files)
