import subprocess


class TrajectoryService:
    def load_trajectory(self, trajectory):
        # trajectory load 처리 예시
        return trajectory

    def run_trajectory(self, trajectory):
        # 실제 실행이 필요하면 별도 프로세스/스레드로 실행
        subprocess.Popen(["echo", f"Running {trajectory}"])
