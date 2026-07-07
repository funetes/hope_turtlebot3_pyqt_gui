from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


class CmdVelViewModel(QObject):
    status_changed = pyqtSignal(str)
    velocity_changed = pyqtSignal(float, float)

    def __init__(self, cmd_vel_service):
        super().__init__()
        self.cmd_vel_service = cmd_vel_service
        self.linear = 0.10
        self.angular = 0.50

    @pyqtSlot()
    def left(self):
        self._send_command("left")

    @pyqtSlot()
    def stop(self):
        self._send_command("stop")

    @pyqtSlot()
    def right(self):
        self._send_command("right")

    @pyqtSlot()
    def forward(self):
        self._send_command("forward")

    @pyqtSlot()
    def backward(self):
        self._send_command("backward")

    @pyqtSlot(float, float)
    def set_velocity(self, linear, angular):
        self.linear = linear
        self.angular = angular
        self.velocity_changed.emit(self.linear, self.angular)

    def _send_command(self, command):
        self.cmd_vel_service.send_command(command, self.linear, self.angular)
        self.status_changed.emit(f"Command: {command} sent")
