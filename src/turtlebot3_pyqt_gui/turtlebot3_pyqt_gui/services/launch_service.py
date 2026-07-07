import subprocess

ROBOT_USER = "hope"
ROBOT_IP = "192.168.250.11"

ROBOT = f"{ROBOT_USER}@{ROBOT_IP}"


class LaunchService:
    def __init__(self):
        self.processes = {}

    def run_bringup(self):
        self._start_process("bringup", ["ros2", "launch", "turtlebot3_bringup", "bringup.launch.py"])

    def run_slam(self):
        self._start_process("slam", ["ros2", "launch", "turtlebot3_slam", "slam.launch.py"])

    def run_nav2(self):
        self._start_process("nav2", ["ros2", "launch", "nav2_bringup", "bringup.launch.py"])

    def run_rviz2(self):
        self._start_process("rviz2", ["rviz2"])

    def save_map(self):
        self._start_process("save_map", ["ros2", "run", "nav2_map_server", "map_saver_cli", "-f", "map"])

    def stop_launches(self):
        for name, proc in list(self.processes.items()):
            proc.terminate()
            proc.wait(timeout=5)
            del self.processes[name]

    def _start_process(self, name, command):
        if name in self.processes:
            raise RuntimeError(f"Process {name} is already running")
        proc = subprocess.Popen(command)
        self.processes[name] = proc
