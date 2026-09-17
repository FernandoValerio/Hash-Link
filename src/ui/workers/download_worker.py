from PySide6.QtCore import QObject,Signal
class DownloadWorker(QObject):
    progress=Signal(int,int)
    finished=Signal(str)
