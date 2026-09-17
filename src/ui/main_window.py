from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import (
    QMainWindow,
    QMenu,
    QMessageBox,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QFrame,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QStackedWidget,
    QSizePolicy,
)

from src.ui.pages.acquisition_page import AcquisitionPage
from src.ui.pages.history_page import HistoryPage
from src.ui.pages.results_page import ResultsPage
from src.ui.pages.settings_page import SettingsPage

APP_VERSION = "0.1.0"

# Índices das páginas — usados pela navegação lateral e pelos itens de menu.
TAB_ACQUISITION = 0
TAB_RESULTS = 1
TAB_HISTORY = 2
TAB_SETTINGS = 3

NAV_ITEMS = [
    ("Aquisição", "Analisar uma URL e selecionar arquivos"),
    ("Resultados", "Hashes calculados nesta sessão"),
    ("Histórico", "Aquisições anteriores"),
    ("Configurações", "Preferências do aplicativo"),
]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hash Link")
        icon_path = Path(__file__).parent / "assets" / "icon.ico"
        self.setWindowIcon(QIcon(str(icon_path)))
        self.resize(1180, 720)
        self.setMinimumSize(960, 600)

        central = QWidget()
        central.setObjectName("CentralHost")
        root_layout = QHBoxLayout(central)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        root_layout.addWidget(self._build_sidebar())
        root_layout.addWidget(self._build_content_area(), stretch=1)

        self.setCentralWidget(central)

        self._create_menu_bar()

        self.statusBar().showMessage("Pronto")

    # ------------------------------------------------------------------
    # Sidebar
    # ------------------------------------------------------------------
    def _build_sidebar(self):
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(232)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        brand_title = QLabel("🔗 Hash Link")
        brand_title.setObjectName("BrandTitle")
        layout.addWidget(brand_title)

        brand_subtitle = QLabel("AQUISIÇÃO & INTEGRIDADE")
        brand_subtitle.setObjectName("BrandSubtitle")
        layout.addWidget(brand_subtitle)

        self.nav_list = QListWidget()
        self.nav_list.setObjectName("NavList")
        self.nav_list.setFrameShape(QFrame.NoFrame)
        self.nav_list.setFocusPolicy(Qt.NoFocus)

        for title, _hint in NAV_ITEMS:
            item = QListWidgetItem(title)
            item.setSizeHint(item.sizeHint())
            self.nav_list.addItem(item)

        self.nav_list.currentRowChanged.connect(self._on_nav_changed)
        layout.addWidget(self.nav_list, stretch=1)

        version_tag = QLabel(f"v{APP_VERSION}")
        version_tag.setObjectName("VersionTag")
        layout.addWidget(version_tag)

        return sidebar

    # ------------------------------------------------------------------
    # Área de conteúdo (header + páginas)
    # ------------------------------------------------------------------
    def _build_content_area(self):
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.header_bar = self._build_header_bar()
        layout.addWidget(self.header_bar)

        self.stack = QStackedWidget()

        self.results_page = ResultsPage()
        self.acquisition_page = AcquisitionPage(self.results_page)
        self.history_page = HistoryPage()
        self.settings_page = SettingsPage()

        self.stack.addWidget(self.acquisition_page)
        self.stack.addWidget(self.results_page)
        self.stack.addWidget(self.history_page)
        self.stack.addWidget(self.settings_page)

        stack_container = QWidget()
        stack_layout = QVBoxLayout(stack_container)
        stack_layout.setContentsMargins(26, 18, 26, 22)
        stack_layout.addWidget(self.stack)
        layout.addWidget(stack_container, stretch=1)

        self.nav_list.setCurrentRow(TAB_ACQUISITION)

        return content

    def _build_header_bar(self):
        header = QFrame()
        header.setObjectName("HeaderBar")

        outer = QVBoxLayout(header)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        top_row = QHBoxLayout()
        top_row.setContentsMargins(0, 0, 0, 0)

        self.page_title_label = QLabel(NAV_ITEMS[0][0])
        self.page_title_label.setObjectName("PageTitle")
        top_row.addWidget(self.page_title_label)
        top_row.addStretch(1)

        status_badge = QLabel("● Pronto")
        status_badge.setObjectName("StatusBadgeReady")
        status_badge.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        top_row.addWidget(status_badge, alignment=Qt.AlignVCenter)

        top_row_widget = QWidget()
        top_row_widget.setLayout(top_row)
        top_row.setContentsMargins(26, 6, 20, 0)
        outer.addWidget(top_row_widget)

        self.page_subtitle_label = QLabel(NAV_ITEMS[0][1])
        self.page_subtitle_label.setObjectName("PageSubtitle")
        outer.addWidget(self.page_subtitle_label)

        return header

    def _on_nav_changed(self, index):
        if index < 0:
            return
        self.stack.setCurrentIndex(index)
        title, hint = NAV_ITEMS[index]
        self.page_title_label.setText(title)
        self.page_subtitle_label.setText(hint)

    # ------------------------------------------------------------------
    # Menu
    # ------------------------------------------------------------------
    def _create_menu_bar(self):
        """Monta a barra de menu superior.

        Por hora apenas os menus **Arquivo** e **Help** existem. Novos
        menus (ex.: Editar, Ferramentas) devem ser adicionados aqui
        seguindo o mesmo padrão: criar o QMenu a partir de
        ``menu_bar.addMenu("&Nome")`` e popular com QAction.
        """
        menu_bar = self.menuBar()

        menu_bar.addMenu(self._build_file_menu())
        menu_bar.addMenu(self._build_help_menu())

    def _build_file_menu(self):
        # "&Arquivo" -> Alt+A abre o menu; o "A" sublinhado é o mnemônico.
        file_menu = QMenu("&Arquivo", self)

        new_acquisition_action = QAction("&Nova aquisição", self)
        new_acquisition_action.setShortcut(QKeySequence("Ctrl+N"))
        new_acquisition_action.setStatusTip("Iniciar uma nova aquisição")
        new_acquisition_action.triggered.connect(self._go_to_acquisition)
        file_menu.addAction(new_acquisition_action)

        open_history_action = QAction("Abrir &histórico", self)
        open_history_action.setShortcut(QKeySequence("Ctrl+H"))
        open_history_action.setStatusTip("Consultar aquisições anteriores")
        open_history_action.triggered.connect(self._go_to_history)
        file_menu.addAction(open_history_action)

        file_menu.addSeparator()

        settings_action = QAction("&Configurações", self)
        settings_action.setStatusTip("Abrir as configurações do programa")
        settings_action.triggered.connect(self._go_to_settings)
        file_menu.addAction(settings_action)

        file_menu.addSeparator()

        exit_action = QAction("Sai&r", self)
        exit_action.setShortcut(QKeySequence("Ctrl+Q"))
        exit_action.setStatusTip("Fechar o Hash Link")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        return file_menu

    def _build_help_menu(self):
        # "&Help" -> Alt+H abre o menu; o "H" sublinhado é o mnemônico.
        help_menu = QMenu("&Help", self)

        about_action = QAction("&Sobre o Hash Link", self)
        about_action.setStatusTip("Informações sobre o programa")
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

        docs_action = QAction("&Documentação", self)
        docs_action.setStatusTip("Abrir a documentação do projeto")
        docs_action.triggered.connect(self._show_docs_info)
        help_menu.addAction(docs_action)

        return help_menu

    # ------------------------------------------------------------------
    # Slots
    # ------------------------------------------------------------------
    def _go_to_acquisition(self):
        self.nav_list.setCurrentRow(TAB_ACQUISITION)

    def _go_to_history(self):
        self.nav_list.setCurrentRow(TAB_HISTORY)

    def _go_to_settings(self):
        self.nav_list.setCurrentRow(TAB_SETTINGS)

    def _show_about(self):
        QMessageBox.about(
            self,
            "Sobre o Hash Link",
            "<b>Hash Link</b><br>"
            f"Versão {APP_VERSION}<br><br>"
            "Aplicação para aquisição, identificação, preservação e "
            "cálculo de hashes criptográficos de arquivos disponibilizados "
            "através de URLs.<br><br>"
            "Desenvolvido por Fernando Valerio."
        )

    def _show_docs_info(self):
        QMessageBox.information(
            self,
            "Documentação",
            "A documentação do projeto está disponível na pasta "
            "'docs/' do repositório:\n\n"
            "• architecture.md\n"
            "• domain-model.md\n"
            "• ui-design.md\n"
            "• developer-guide.md\n"
            "• user-guide.md",
        )
