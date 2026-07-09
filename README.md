# TurtleBot3 PyQt GUI

## 프로젝트 이름

TurtleBot3 PyQt GUI for ROS 2 Humble

## 프로젝트 소개

이 프로젝트는 TurtleBot3 Burger를 ROS 2 Humble 환경에서 편리하게 모니터링하고 제어하기 위한 PyQt 기반 GUI 애플리케이션입니다.

주요 기능은 다음과 같습니다.

- 로봇 상태 및 배터리/전압 정보 표시
- /cmd_vel, /odom, /scan 등 주요 토픽 모니터링
- 경유점(Waypoint) 등록 및 선택 이동
- trajectory 파일 로딩 및 다중 경로 실행
- gTTS 기반 음성 출력
- bringup, Nav2, RViz, SLAM, 맵 저장 등 런치 제어
- 실행 로그 ~~및 팀별 확장 기능 영역 제공~~

## 팀명 및 팀원

- 팀명: Hope
- 팀원: 김환, 박창민

## 개발 환경

- OS: Ubuntu 22.04(Linux)
- ROS 2: Humble
- Python: 3.10+
- GUI Framework: PyQt5
- Robot Platform: TurtleBot3 Burger
- 통신: ROS 2 topic / action / SSH(remote launch)

## 설치해야 하는 패키지

### 1) ROS 2 및 TurtleBot3 관련 패키지

- ROS 2 Humble
- TurtleBot3 
- navagation2
- cartographer
- rviz2

### 2) Python 패키지

```bash
sudo apt update
sudo apt install -y python3-pyqt5 python3-pyqt5.qtsvg python3-yaml
```

## 패키지 빌드 방법

```bash
cd /home/$USER/hope_turtlebot3_pyqt_gui
source /opt/ros/humble/setup.bash
colcon build
source install/setup.bash
```

## 실행 방법

빌드가 완료된 후 아래 명령으로 실행합니다.

```bash
ros2 run turtlebot3_pyqt_gui turtlebot3_gui
```

실행 전에 ROS_DOMAIN_ID와 네트워크 환경이 정상인지 확인하는 것이 좋습니다.

## GUI 사용 방법

실행 후 메인 윈도우에서 다음 영역을 사용할 수 있습니다.

### 로봇 상태 영역

- Connect: ROS 환경 연결 상태를 반영합니다.
- Disconnect: 연결 상태를 해제합니다.
- Exit: GUI를 종료합니다.

### 배터리/전압 영역

- 배터리 잔량과 전압을 확인합니다.

### TOPIC 모니터링 영역

- 현재위치 x
- 현재위치 y
- 현재방향 yaw
- Lidar 최소 거리 

### Waypoint 영역

- Load YAML 버튼으로 waypoint 파일을 불러옵니다.
- nav2가 실행된 상태에서 경유점을 선택하고 Go To Waypoint를 눌러 이동합니다.

### Trajectory 영역

- nav2를 실행시킵니다.
- Load 버튼으로 trajectory YAML 파일을 불러옵니다.
- ComboBox에서 trajectory를 선택합니다.
- nav2가 실행된 상태에서 Run 버튼으로 실행합니다.

### 5) gTTS 영역

- 텍스트 입력창에 문장을 입력합니다.
- Speak 버튼을 누르면 음성 출력 요청이 전달됩니다.

### 6) Launch Control 영역

- Run Bringup: 로봇에서 bringup 실행
- Run Nav2: Nav2 실행
- Run SLAM: SLAM 실행
- Run Rviz2: RViz 실행
- Save Map: 현재 맵 저장 (현재 맵은 hope_연일월시_map.yaml 형식으로 /home/maps에 저장됩니다.)
- Stop Launches: 실행 중인 launch 종료

## 주요 기능 설명

- 로봇 상태 모니터링
  - ROS 연결 상태, 배터리/전압, 이동 명령값, 위치/방향/거리 정보 확인 가능
- 경유점 이동
  - YAML로 정의한 waypoint를 불러와 원하는 지점으로 이동 가능
- Trajectory 실행
  - 여러 waypoint를 묶은 trajectory를 선택해 순차 이동 가능
- 음성 출력
  - 입력한 문자열을 음성으로 출력하는 기능 제공
- 프로세스 제어
  - 로봇 런치와 네비게이션 관련 프로세스를 GUI에서 제어 가능

## 경유점 실행 방법

waypoint YAML 파일은 다음 형식으로 작성합니다.

```yaml
waypoints:
  - name: point1
    frame_id: map
    pose:
      position:
        x: 1.0
        y: 2.0
        z: 0.0
      angle:
        yaw: 0.0
  - name: point2
    frame_id: map
    pose:
      position:
        x: 2.0
        y: 3.0
        z: 0.0
      angle:
        yaw: 1.57
```

로드 후 Waypoint ComboBox에서 선택하고 **Go To Waypoint**를 누르면 이동합니다.

## trajectory 실행 방법

trajectory YAML 파일은 다음 형식으로 작성합니다.

```yaml
waypoints:
  - name: point1
    frame_id: map
    pose:
      position:
        x: 1.0
        y: 2.0
        z: 0.0
      angle:
        yaw: 0.0
  - name: point2
    frame_id: map
    pose:
      position:
        x: 2.0
        y: 3.0
        z: 0.0
      angle:
        yaw: 1.57

trajectories:
  - name: route_a
    waypoints:
      - point1
      - point2
```

로드 후 trajectory를 선택하고 **Run** 버튼을 누르면 실행됩니다.

## gTTS 사용 방법

1. gTTS 영역의 입력창에 원하는 문장을 입력합니다.
2. Speak 버튼을 누릅니다.
3. GUI가 음성 요청을 전달하면, 로봇 측 오디오 노드가 해당 문장을 재생합니다.

## bringup/nav2/teleop 버튼 사용 방법

현재 구현 기준으로는 다음 버튼이 동작합니다.

- Run Bringup: 로봇 bringup 실행
- Run Nav2: Nav2 실행
- Run Rviz2: RViz 실행
- Run SLAM: SLAM 실행
- Save Map: 맵 저장
- Stop Launches: 실행 중인 launch 종료

## 로그 확인 방법

하단의 Log 영역에서 GUI 동작과 상태 변화를 확인할 수 있습니다.

- [TTS] : 음성 출력 관련 메시지
- [CMD_VEL] : 속도 명령 메시지
- [PROCESS] : 런치/프로세스 상태 메시지
- [WAYPOINT] : waypoint 관련 동작 로그

## 팀별 추가 기능 설명

- 

## 주의 사항(옵션)

- 실제 로봇과 연결할 때는 SSH 접속이 가능해야 합니다.
- 로봇 IP와 사용자 정보가 코드에 맞게 설정되어 있어야 합니다.
- Nav2/bringup 실행 전에는 로봇의 센서, 모터, IMU 상태가 정상인지 확인하는 것이 좋습니다.
- ROS_DOMAIN_ID가 서로 다르면 토픽 통신이 되지 않을 수 있습니다.

## 실행 화면 예시

아래와 같은 형태로 GUI가 구성됩니다.

```text
[Robot Status] [Battery / Voltage] [Launch Control]
[Waypoint]     [Trajectory]       [gTTS]
[Velocity / Topic Monitor]
[Log / Team Custom Functions]
```

## 참고

이 프로젝트는 ROS 2 기반 TurtleBot3 제어를 GUI로 단순화하여 실험과 데모에 활용하기 좋도록 설계되었습니다.
