from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


class GttsViewModel(QObject):
    speak_requested = pyqtSignal(str)
    status_changed = pyqtSignal(str)

    def __init__(self, gtts_service):
        super().__init__()
        self.gtts_service = gtts_service

    @pyqtSlot(str)
    def speak(self, text):
        if not text:
            self.status_changed.emit("Please enter text.")
            return
        self.status_changed.emit("Speaking...")
        self.gtts_service.speak(text)
        self.status_changed.emit("Speak request submitted.")
