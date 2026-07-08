from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from sensor_msgs.msg import BatteryState

from signals.RosSignalsManager import SignalsManager


class BatteryVoltageViewModel(QObject):
    status_changed = pyqtSignal(str, int)

    def __init__(self):
        super().__init__()

        # 싱글턴 인스턴스 획득
        self.signal_manager = SignalsManager

        self.signal_manager.battery_status_received.connect(self.update_battery_state)

    @pyqtSlot(str, str, int)
    def update_status(self, voltage, percentage):
        self.status_changed.emit(voltage, percentage)

    def update_battery_state(self, battery_state: BatteryState):

        volt = battery_state.voltage
        percentage = int(battery_state.percentage)

        if percentage < 0:
            percentage = 0

        if percentage > 100:
            percentage = 100

        self.update_status(f"{volt:.1f} V", percentage)
        # print(f"Battery: {percentage} %")
        # print(int(percentage))
