from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QTextEdit


class LogWidget(QWidget):
    def __init__(self, viewmodel=None):
        super().__init__()
        self.viewmodel = None

        layout = QVBoxLayout(self)

        log_group = QGroupBox("Log Output")
        log_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        log_layout = QVBoxLayout()

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setPlainText("System initialized.\nWaiting for commands...")

        log_layout.addWidget(self.log_text)
        log_group.setLayout(log_layout)
        layout.addWidget(log_group)

        if viewmodel is not None:
            self.set_viewmodel(viewmodel)

    def set_viewmodel(self, viewmodel):
        self.viewmodel = viewmodel
        self.viewmodel.log_updated.connect(self._append_log)

    def _append_log(self, message):
        self.log_text.append(message)
