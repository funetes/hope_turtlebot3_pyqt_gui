import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout
from services.launch_service import LaunchService
from services.gtts_service import GttsService
from services.trajectory_service import TrajectoryService
from services.cmd_vel_service import CmdVelService
from viewmodels.process_control_viewmodel import ProcessControlViewModel
from viewmodels.gtts_viewmodel import GttsViewModel
from viewmodels.trajectory_viewmodel import TrajectoryViewModel
from viewmodels.cmd_vel_viewmodel import CmdVelViewModel
from viewmodels.robot_status_viewmodel import RobotStatusViewModel
from viewmodels.battery_viewmodel import BatteryViewModel
from viewmodels.battery_voltage_viewmodel import BatteryVoltageViewModel
from viewmodels.ros2_topic_viewmodel import Ros2TopicViewModel
from viewmodels.waypoint_viewmodel import WaypointViewModel
from viewmodels.log_viewmodel import LogViewModel
from viewmodels.team_custom_viewmodel import TeamCustomViewModel
from ui.robot_status_widget import RobotStatusWidget
from ui.battery_voltage_widget import BatteryVoltageWidget
from ui.cmd_vel_widget import CmdVelWidget
from ui.ros2_topic_widget import Ros2TopicWidget
from ui.waypoint_widget import WaypointWidget
from ui.trajectory_widget import TrajectoryWidget
from ui.gtts_widget import GttsWidget
from ui.process_control_widget import ProcessControlWidget
from ui.log_widget import LogWidget
from ui.team_custom_widget import TeamCustomWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TurtleBot3 Burger ROS2 Humble Control GUI")
        self.resize(1200, 820)

        self.launch_service = LaunchService()
        self.gtts_service = GttsService()
        self.trajectory_service = TrajectoryService()
        self.cmd_vel_service = CmdVelService()

        self.process_viewmodel = ProcessControlViewModel(self.launch_service)
        self.gtts_viewmodel = GttsViewModel(self.gtts_service)
        self.trajectory_viewmodel = TrajectoryViewModel(self.trajectory_service)
        self.cmd_vel_viewmodel = CmdVelViewModel(self.cmd_vel_service)
        self.robot_status_viewmodel = RobotStatusViewModel()
        self.battery_viewmodel = BatteryViewModel()
        self.battery_voltage_viewmodel = BatteryVoltageViewModel()
        self.ros2_topic_viewmodel = Ros2TopicViewModel()
        self.waypoint_viewmodel = WaypointViewModel()
        self.log_viewmodel = LogViewModel()
        self.team_custom_viewmodel = TeamCustomViewModel()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QGridLayout(central_widget)

        self.init_status_ui(main_layout)
        self.init_monitor_ui(main_layout)
        self.init_navigation_ui(main_layout)
        self.init_utils_ui(main_layout)

    def init_status_ui(self, layout):
        self.init_robot_status_area(layout)
        self.init_battery_voltage_area(layout)

    def init_monitor_ui(self, layout):
        self.init_cmd_vel_area(layout)
        self.init_ros2_topic_monitor_area(layout)

    def init_navigation_ui(self, layout):
        self.init_waypoint_area(layout)
        self.init_trajectory_area(layout)

    def init_utils_ui(self, layout):
        self.init_gtts_area(layout)
        self.init_process_control_area(layout)
        self.init_log_area(layout)
        self.init_team_custom_area(layout)

    def init_robot_status_area(self, layout):
        layout.addWidget(RobotStatusWidget(self.robot_status_viewmodel), 0, 0)

    def init_battery_voltage_area(self, layout):
        layout.addWidget(BatteryVoltageWidget(self.battery_voltage_viewmodel), 0, 1)

    def init_cmd_vel_area(self, layout):
        layout.addWidget(CmdVelWidget(self.cmd_vel_viewmodel), 1, 0)

    def init_ros2_topic_monitor_area(self, layout):
        layout.addWidget(Ros2TopicWidget(self.ros2_topic_viewmodel), 1, 1)

    def init_waypoint_area(self, layout):
        layout.addWidget(WaypointWidget(self.waypoint_viewmodel), 2, 0)

    def init_trajectory_area(self, layout):
        layout.addWidget(TrajectoryWidget(self.trajectory_viewmodel), 2, 1)

    def init_gtts_area(self, layout):
        layout.addWidget(GttsWidget(self.gtts_viewmodel), 3, 0)

    def init_process_control_area(self, layout):
        layout.addWidget(ProcessControlWidget(self.process_viewmodel), 3, 1)

    def init_log_area(self, layout):
        layout.addWidget(LogWidget(self.log_viewmodel), 4, 0, 1, 2)

    def init_team_custom_area(self, layout):
        layout.addWidget(TeamCustomWidget(self.team_custom_viewmodel), 5, 0, 1, 2)


def main():
    app = QApplication([])
    win = MainWindow()
    win.show()
    app.exec_()

if __name__ == "__main__":
    main()