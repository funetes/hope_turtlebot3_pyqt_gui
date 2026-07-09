from PyQt5.QtCore import QObject, pyqtSignal
from ..signals.RosSignalsManager import SignalsManager

class LogViewModel(QObject):
    log_updated = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.signal_manager = SignalsManager
        self.signal_manager.log_msg_rceived.connect(self.append_log)

    def append_log(self, message):
        self.log_updated.emit(message)

    
