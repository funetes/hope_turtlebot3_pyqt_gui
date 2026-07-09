from robot_audio_interfaces.msg import AudioCommand
from PyQt5.QtCore import QProcess

class GttsService:
    def __init__(self, node=None):
        self._node = node
        self._publisher = None
        self._audio_process = None
        self._status_process = None
        self._status_callback = None
        self._status_output = ""
        self._status_error = ""
        self.processes = {}
        self._init_publisher()
    
    def _init_publisher(self):
        if self._node is None:
            return
        self._publisher = self._node.create_publisher(
            AudioCommand,
            '/audio/command',
            10
        )

    def _create_status_process(self):
        self._status_process = QProcess()
        self._status_process.setProcessChannelMode(QProcess.MergedChannels)
        self._status_process.readyReadStandardOutput.connect(self._on_status_stdout)
        self._status_process.readyReadStandardError.connect(self._on_status_stderr)
        self._status_process.finished.connect(self._on_status_finished)

    def _create_audio_process(self):
        self._audio_process = QProcess()
        self._audio_process.setProcessChannelMode(QProcess.MergedChannels)
        self._audio_process.readyReadStandardOutput.connect(
            lambda: print("[STDOUT]:", bytes(self._audio_process.readAllStandardOutput()).decode('utf-8', 'replace'))
        )
        self._audio_process.readyReadStandardError.connect(
            lambda: print("[STDERR]: ", bytes(self._audio_process.readAllStandardError()).decode('utf-8', 'replace'))
        )

    def connect_audio(self, status_callback):
        self._status_callback = status_callback
        self._status_output = ""
        self._status_error = ""

        if self._status_process is None:
            self._create_status_process()

        if self._status_process.state() != QProcess.NotRunning:
            return

        self._status_process.start("ssh", [
            "hope@192.168.250.11",
            "/bin/bash", "-lc",
            "~/tb3_scripts/status_audio.sh"
        ])

        if callable(self._status_callback):
            self._status_callback("checking audio status...")

    def _on_status_stdout(self):
        self._status_output += bytes(self._status_process.readAllStandardOutput()).decode('utf-8', 'replace')

    def _on_status_stderr(self):
        self._status_error += bytes(self._status_process.readAllStandardError()).decode('utf-8', 'replace')

    def _on_status_finished(self, exit_code, exit_status):
        status = self._status_output.strip()

        if self._status_error:
            if callable(self._status_callback):
                self._status_callback(f"audio status error: {self._status_error.strip()}")
            return

        if status == "RUNNING":
            if callable(self._status_callback):
                self._status_callback("")
            return

        if callable(self._status_callback):
            self._status_callback("audio stopped, starting audio node...")
        self._start_audio_node()

    def _start_audio_node(self):
        if self._audio_process is None:
            self._create_audio_process()

        if self._audio_process.state() != QProcess.NotRunning:
            return

        self._audio_process.start("ssh", [
            "hope@192.168.250.11",
            "/bin/bash", "-lc",
            "~/tb3_scripts/run_audio.sh"
        ])

        if callable(self._status_callback):
            self._status_callback("audio node started")

    def speak(self, text):
        if self._publisher is None:
            self._init_publisher()

        if self._publisher is None:
            return

        print(f'{text} printed')
        msg = AudioCommand()
        msg.type = AudioCommand.TYPE_TTS
        msg.text = text
        msg.volume = 0.3
        msg.repeat = 1
    
        self._publisher.publish(msg)

        if callable(self._status_callback):
            self._status_callback("")

