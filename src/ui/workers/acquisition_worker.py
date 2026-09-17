from PySide6.QtCore import QObject,Signal
class AcquisitionWorker(QObject):
    finished=Signal(object)
    error=Signal(str)
