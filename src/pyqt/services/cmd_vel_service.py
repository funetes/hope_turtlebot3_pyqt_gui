import subprocess


class CmdVelService:
    def send_command(self, command, linear, angular):
        # ROS2 cmd_vel 퍼블리시 예시
        subprocess.Popen(["echo", f"{command} linear={linear} angular={angular}"])
