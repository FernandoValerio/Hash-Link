import shutil
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
    QFileDialog,
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
    def __init__(self, results_page, metadata_page):
        super().__init__()
        self.results_page = results_page
        self.metadata_page = metadata_page

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

        self.analyse.clicked.connect(self.analyse_source)
        self.browse_file_button.clicked.connect(self.browse_file)
        self.browse_folder_button.clicked.connect(self.browse_folder)
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

        hint = QLabel(
            "Informe uma URL ou um caminho local (arquivo ou pasta) para descobrir "
            "os arquivos disponíveis. O tipo é reconhecido automaticamente."
        )
        hint.setProperty("class", "CardHint")
        inner.addWidget(hint)

        row = QHBoxLayout()
        row.setSpacing(10)

        self.url = QLineEdit()
        self.url.setPlaceholderText("https://... ou C:\\caminho\\arquivo (ou pasta)")
        self.url.setMinimumHeight(38)
        row.addWidget(self.url, stretch=1)

        self.browse_file_button = QPushButton("📄 Arquivo...")
        self.browse_file_button.setObjectName("SecondaryButton")
        self.browse_file_button.setMinimumHeight(38)
        self.browse_file_button.setCursor(Qt.PointingHandCursor)
        row.addWidget(self.browse_file_button)

        self.browse_folder_button = QPushButton("📁 Pasta...")
        self.browse_folder_button.setObjectName("SecondaryButton")
        self.browse_folder_button.setMinimumHeight(38)
        self.browse_folder_button.setCursor(Qt.PointingHandCursor)
        row.addWidget(self.browse_folder_button)

        self.analyse = QPushButton("🔍  Analisar")
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
            "Nenhum arquivo listado ainda.\n"
            "Informe uma URL ou um caminho local acima e clique em “Analisar”."
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
    # Lógica
    # ------------------------------------------------------------------
    def browse_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Selecionar arquivo")
        if path:
            self.url.setText(path)

    def browse_folder(self):
        path = QFileDialog.getExistingDirectory(self, "Selecionar pasta")
        if path:
            self.url.setText(path)

    def analyse_source(self):
        source = self.url.text().strip()

        try:
            service = AcquisitionService()

            result = service.analyse(source)

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

    def _materialize(self, file, destination: Path):
        """Coloca o conteúdo de `file` em `destination`: baixa via HTTP se for um
        link, ou copia do disco (preservando metadados, com copy2) se `file` for
        local — reconhecido por `file.is_local`."""
        destination.parent.mkdir(parents=True, exist_ok=True)
        if file.is_local:
            shutil.copy2(file.local_path, destination)
            self.progress_bar.setValue(100)
        else:
            session = Session()
            downloader = Downloader()
            downloader.download(
                session=session,
                url=file.url,
                destination=str(destination),
                callback=self.progress,
            )

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

        for file in selected_files:
            self.progress_bar.setValue(0)
            destination = Path(OUTPUT) / file.name
            self._materialize(file, destination)
            self.metadata_page.add_file(destination)
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
        hash_tipeA = "MD5"
        hash_tipeB = "SHA-256"
        for file in selected_files:
            destination = Path(HASH) / file.name
            self._materialize(file, destination)
        for file in selected_files:
            local_file = Path(HASH) / file.name

            if not local_file.exists():
                continue
            hash_A = calculate_hash(local_file, hash_tipeA)
            hash_B = calculate_hash(local_file, hash_tipeB)
            self.results_page.add_result(
                file.name,
                hash_A,
                hash_B
            )

        print(selected_files)