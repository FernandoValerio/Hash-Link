from PySide6.QtWidgets import QWidget,QVBoxLayout,QProgressBar
class ProgressWidget(QWidget):
    def __init__(self):
        super().__init__()
        l=QVBoxLayout(self)
        self.progress=QProgressBar()
        l.addWidget(self.progress)
