import os
from PyQt5.QtCore import QProcess
from datetime import datetime

ROBOT_USER = "hope"
ROBOT_IP = "192.168.250.11"
ROBOT = f"{ROBOT_USER}@{ROBOT_IP}"
TIME = datetime.now().strftime("%Y%m%d%H%M%S")
HOME = os.path.expanduser("~")

class LaunchService:
    def __init__(self):
        self.processes = {}
        self.viewmodel = None

    def set_viewmodel(self, viewmodel):
        self.viewmodel = viewmodel

    def run_bringup(self):
        self._start_remote_process(
            "bringup", 
            ["~/tb3_scripts/start_bringup.sh"]
        )
    
    def stop_bringup(self):
        self._start_remote_process(
            "stop_bringup", 
            ["~/tb3_scripts/stop_bringup.sh"]
        )

    def status_bringup(self):
        self._start_remote_process(
            "status_bringup",
            ["~/tb3_scripts/status_bringup.sh"]
        )

    def run_slam(self):
        self._start_local_process(
            "slam", 
            ["ros2", "launch", "turtlebot3_cartographer", "cartographer.launch.py", "use_sim_time:=false"]
        )

    def run_nav2(self):
        self._start_local_process(
            "nav2", 
            ["ros2", 
             "launch", 
             "turtlebot3_navigation2", 
             "navigation2.launch.py", 
             f"map:={HOME}/maps/hope.yaml", 
             f"params_file:={HOME}/turtlebot3_ws/src/turtlebot3/turtlebot3_navigation2/param/humble/burger.yaml"
            ]
        )

    def run_rviz2(self):
        self._start_local_process(
            "rviz2", 
            ["rviz2"]
        )

    def save_map(self):
        self._start_local_process(
            "save_map", 
            ["ros2", "run", "nav2_map_server", "map_saver_cli", "-f", f"{HOME}/maps/hope_{TIME}_map"]
        )

    def stop_launches(self):
        for name, proc in list(self.processes.items()):
            if proc.state() != QProcess.NotRunning:
                proc.terminate()
                proc.waitForFinished(5000)
            del self.processes[name]

    def _start_local_process(self, name, command):
        if not command:
            raise ValueError("Command list cannot be empty")

        proc = QProcess()
        proc.start(command[0], command[1:])
        self.processes[name] = proc
        return proc

    def _start_remote_process(self, name, command):
        if not command:
            raise ValueError("Remote command list cannot be empty")

        proc = QProcess()
        proc.readyReadStandardOutput.connect(lambda: self._on_stdout_ready(name, proc))
        proc.readyReadStandardError.connect(lambda: self._on_stderr_ready(name, proc))
        ssh_command = [ROBOT, ' '.join(command)]
        proc.start("ssh", ssh_command)
        self.processes[name] = proc
        return proc
    
    def _on_stdout_ready(self, name, proc):
        data = proc.readAllStandardOutput().data().decode()
        if data:
            print(f"[{name}] {data}", end="")
            if self.viewmodel is not None:
                self.viewmodel.status_changed.emit(data.strip())

    def _on_stderr_ready(self, name, proc):
        data = proc.readAllStandardError().data().decode()
        if data:
            print(f"[{name}][ERR] {data}", end="")
            if self.viewmodel is not None:
                self.viewmodel.status_changed.emit(data.strip())
