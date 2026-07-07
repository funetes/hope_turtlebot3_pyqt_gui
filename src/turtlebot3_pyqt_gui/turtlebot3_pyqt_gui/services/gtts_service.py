import subprocess


class GttsService:
    def speak(self, text):
        # 실제 gTTS 처리는 별도 스레드나 서비스로 이전 가능
        # 여기서는 예시로 로컬 명령 실행 형태를 둔다.
        subprocess.Popen(["python3", "-c", f'print("{text}")'])
