from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QLabel, QPushButton, QHBoxLayout


class TeamCustomWidget(QWidget):
    def __init__(self, viewmodel=None):
        super().__init__()
        self.viewmodel = None

        layout = QVBoxLayout(self)

        custom_group = QGroupBox("Team Custom Functions")
        custom_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        custom_layout = QVBoxLayout()

        custom_layout.addWidget(QLabel("Use this area to add team-specific tools."))

        button_row = QHBoxLayout()
        self.btn_custom1 = QPushButton("Custom 1")
        self.btn_custom2 = QPushButton("Custom 2")
        button_row.addWidget(self.btn_custom1)
        button_row.addWidget(self.btn_custom2)
        custom_layout.addLayout(button_row)

        custom_group.setLayout(custom_layout)
        layout.addWidget(custom_group)

        if viewmodel is not None:
            self.set_viewmodel(viewmodel)

    def set_viewmodel(self, viewmodel):
        self.viewmodel = viewmodel
        self.btn_custom1.clicked.connect(self.viewmodel.custom_1)
        self.btn_custom2.clicked.connect(self.viewmodel.custom_2)
