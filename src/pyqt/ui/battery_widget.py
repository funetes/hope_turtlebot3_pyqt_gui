from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar

class BatteryWidget(QWidget): # QWidget을 상속받아 커스텀 컴포넌트 생성
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        
        self.title = QLabel("🔋 터틀봇 배터리 상태")
        self.progress = QProgressBar()
        self.progress.setValue(100) # 기본값 100%
        
        layout.addWidget(self.title)
        layout.addWidget(self.progress)
        
    def update_status(self, voltage, percentage):
        """ROS 2 데이터가 들어오면 UI를 갱신할 함수"""
        self.title.setText(f"🔋 전압: {voltage}V")
        self.progress.setValue(int(percentage))