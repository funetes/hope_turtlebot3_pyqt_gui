from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QPushButton, QLineEdit, QLabel


class GttsWidget(QWidget):
    def __init__(self, viewmodel=None):
        super().__init__()
        self.viewmodel = None

        layout = QVBoxLayout(self)

        gtts_group = QGroupBox("gTTS Output")
        gtts_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        gtts_layout = QVBoxLayout()

        self.text_input = QLineEdit("Hello TurtleBot")
        self.btn_speak = QPushButton("Speak")
        self.status_label = QLabel("Preprare TTS...")
        gtts_layout.addWidget(self.text_input)
        gtts_layout.addWidget(self.btn_speak)
        gtts_layout.addWidget(self.status_label)

        gtts_group.setLayout(gtts_layout)
        layout.addWidget(gtts_group)

        if viewmodel is not None:
            self.set_viewmodel(viewmodel)

    def set_viewmodel(self, viewmodel):
        self.viewmodel = viewmodel
        self.btn_speak.clicked.connect(self._on_speak_clicked)
        self.viewmodel.speak_requested.connect(self._on_speak_requested)
        self.viewmodel.status_changed.connect(self._on_status_changed)

    def _on_speak_clicked(self):
        if self.viewmodel is None:
            return
        self.viewmodel.speak(self.text_input.text())

    def _on_speak_requested(self, message):
        self.status_label.setText(message)

    def _on_status_changed(self, message):
        self.status_label.setText(message)
