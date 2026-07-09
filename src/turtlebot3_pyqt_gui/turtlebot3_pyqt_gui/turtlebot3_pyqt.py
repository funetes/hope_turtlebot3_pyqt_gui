import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QScrollArea
from .services.launch_service import LaunchService
from .services.gtts_service import GttsService
from .services.trajectory_service import TrajectoryService
from .services.cmd_vel_service import CmdVelService
from .services.waypoints_service import WaypointService
from .viewmodels.process_control_viewmodel import ProcessControlViewModel
from .viewmodels.gtts_viewmodel import GttsViewModel
from .viewmodels.trajectory_viewmodel import TrajectoryViewModel
from .viewmodels.cmd_vel_viewmodel import CmdVelViewModel
from .viewmodels.robot_status_viewmodel import RobotStatusViewModel
from .viewmodels.battery_voltage_viewmodel import BatteryVoltageViewModel
from .viewmodels.ros2_topic_viewmodel import Ros2TopicViewModel
from .viewmodels.waypoint_viewmodel import WaypointViewModel
from .viewmodels.log_viewmodel import LogViewModel
from .viewmodels.team_custom_viewmodel import TeamCustomViewModel
from .ui.robot_status_widget import RobotStatusWidget
from .ui.battery_voltage_widget import BatteryVoltageWidget
from .ui.cmd_vel_widget import CmdVelWidget
from .ui.ros2_topic_widget import Ros2TopicWidget
from .ui.waypoint_widget import WaypointWidget
from .ui.trajectory_widget import TrajectoryWidget
from .ui.gtts_widget import GttsWidget
from .ui.process_control_widget import ProcessControlWidget
from .ui.log_widget import LogWidget
from .ui.team_custom_widget import TeamCustomWidget

class MainWindow(QMainWindow):
    def __init__(self, ros_node=None):
        super().__init__()
        self.setWindowTitle("TurtleBot3 Burger ROS2 Humble Control GUI")
        self.resize(1200, 820)

        self.launch_service = LaunchService()
        self.gtts_service = GttsService(ros_node)
        waypoint_yaml_load_service = WaypointService(ros_node)
        self.trajectory_service = TrajectoryService(ros_node)
        self.cmd_vel_service = CmdVelService(ros_node)

        self.process_viewmodel = ProcessControlViewModel(self.launch_service)
        self.gtts_viewmodel = GttsViewModel(self.gtts_service)
        self.trajectory_viewmodel = TrajectoryViewModel(self.trajectory_service)
        self.cmd_vel_viewmodel = CmdVelViewModel(self.cmd_vel_service)
        self.robot_status_viewmodel = RobotStatusViewModel()
        self.battery_voltage_viewmodel = BatteryVoltageViewModel()
        self.ros2_topic_viewmodel = Ros2TopicViewModel()


        self.waypoint_viewmodel = WaypointViewModel(waypoint_yaml_load_service, ros_node)
        self.log_viewmodel = LogViewModel()
        self.team_custom_viewmodel = TeamCustomViewModel(ros_node)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        scroll_area = QScrollArea(central_widget)
        scroll_area.setWidgetResizable(True)

        content_widget = QWidget()
        scroll_area.setWidget(content_widget)

        main_layout = QGridLayout(content_widget)

        outer_layout = QGridLayout(central_widget)
        outer_layout.addWidget(scroll_area, 0, 0)
        central_widget.setLayout(outer_layout)

        self.init_status_ui(main_layout)
        self.init_monitor_ui(main_layout)
        self.init_navigation_ui(main_layout)
        self.init_utils_ui(main_layout)

        self._connect_viewmodel_logging()

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
        layout.addWidget(CmdVelWidget(self.cmd_vel_viewmodel), 1, 2)

    def init_ros2_topic_monitor_area(self, layout):
        layout.addWidget(Ros2TopicWidget(self.ros2_topic_viewmodel), 1, 1)

    def init_waypoint_area(self, layout):
        layout.addWidget(WaypointWidget(self.waypoint_viewmodel), 1, 0)

    def init_trajectory_area(self, layout):
        layout.addWidget(TrajectoryWidget(self.trajectory_viewmodel), 2, 0)

    def init_gtts_area(self, layout):
        layout.addWidget(GttsWidget(self.gtts_viewmodel), 2, 1, 1, 2)

    def init_process_control_area(self, layout):
        layout.addWidget(ProcessControlWidget(self.process_viewmodel), 0, 2)

    def init_log_area(self, layout):
        layout.addWidget(LogWidget(self.log_viewmodel), 4, 0, 1, 3)

    def init_team_custom_area(self, layout):
        layout.addWidget(TeamCustomWidget(self.team_custom_viewmodel), 5, 0, 1, 3)


    def _connect_viewmodel_logging(self):
        self.gtts_viewmodel.status_changed.connect(
            lambda msg: self.log_viewmodel.append_log(f"[TTS] {msg}")
        )
        self.cmd_vel_viewmodel.status_changed.connect(
            lambda msg: self.log_viewmodel.append_log(f"[CMD_VEL] {msg}")
        )
        self.process_viewmodel.status_changed.connect(
            lambda msg: self.log_viewmodel.append_log(f"[PROCESS] {msg}")
        )
        self.process_viewmodel.error_occurred.connect(
            lambda msg: self.log_viewmodel.append_log(f"[PROCESS][ERROR] {msg}")
        )
        self.waypoint_viewmodel.waypoint_selected.connect(
            lambda msg: self.log_viewmodel.append_log(f"[WAYPOINT] {msg}")
        )
        self.waypoint_viewmodel.waypoint_requested.connect(
            lambda msg: self.log_viewmodel.append_log(f"[WAYPOINT] {msg}")
        )
        self.team_custom_viewmodel.action_triggered.connect(
            lambda msg: self.log_viewmodel.append_log(f"[WEATHER] {msg}")
        )

    def closeEvent(self, event):
        # if self.node:
        #     self.send_velocity(0.0, 0.0)

        # self.stop_processes()
        # self.disconnect_ros()

        # if rclpy.ok():
        #     rclpy.shutdown()
        

        event.accept()

def main():
    app = QApplication([])
    win = MainWindow()
    win.show()
    app.exec_()

if __name__ == "__main__":
    main()
