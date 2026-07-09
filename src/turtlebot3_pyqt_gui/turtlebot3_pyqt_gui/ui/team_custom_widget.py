from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QLabel, QPushButton, QHBoxLayout


class TeamCustomWidget(QWidget):
    def __init__(self, viewmodel=None):
        super().__init__()
        self.viewmodel = None

        layout = QVBoxLayout(self)

        custom_group = QGroupBox("Team Custom Functions")
        custom_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        custom_layout = QVBoxLayout()

        button_row = QHBoxLayout()
        self.btn_custom1 = QPushButton("날씨요정 🌦️")
        button_row.addWidget(self.btn_custom1)
        custom_layout.addLayout(button_row)

        custom_group.setLayout(custom_layout)
        layout.addWidget(custom_group)

        if viewmodel is not None:
            self.set_viewmodel(viewmodel)

    def set_viewmodel(self, viewmodel):
        self.viewmodel = viewmodel
        self.btn_custom1.clicked.connect(self.viewmodel.get_weather)
