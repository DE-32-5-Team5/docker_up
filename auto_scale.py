import subprocess
import json
import time

# 스케일링 조건을 위한 설정
start = 0  # 타이머 초기화
sca = 1  # 현재 컨테이너 개수
lim = 0.03  # CPU 임계값 설정 (예시로 5%로 설정)

try:
    while True:
        # Docker stats를 통해 특정 컨테이너의 CPU 사용량 가져오기
        r = subprocess.run(
            ["docker", "stats", "streamlit_container", "--no-stream", "--format", "{{ json .}}"],
            capture_output=True, text=True
        )
        
        # JSON 형식으로 출력된 CPU 사용량 파싱
        j = json.loads(r.stdout)
        per = float(j["CPUPerc"][:-1])  # '%' 기호 제거 후 float으로 변환
        print(f"현재 CPU 사용량은 {per}%입니다.")

        # 스케일 아웃 조건: CPU 사용률이 임계값을 넘었을 때
        if per > lim:
            if not start:  # 처음 넘은 경우, 시작 시간 기록
                start = time.time()
            else:  # 넘은 상태가 1분 지속되면 스케일 아웃
                end = time.time()
                if end - start >= 60.00:
                    print(f"Container가 임계값을 넘은지 1분이 지났습니다. 현재 컨테이너 개수 : {sca}")
                    sca += 1
                    start = 0  # 스케일 아웃 후 타이머 초기화
                    # docker compose scale 명령어로 컨테이너 수 조정
                    subprocess.run(["docker", "compose", "scale", f"blog={sca}"])

        # 스케일 인 조건: CPU 사용률이 임계값 이하이고, 컨테이너가 2개 이상일 때
        elif per <= lim and sca > 1:
            if not start:  # 처음 조건을 만족한 경우, 시작 시간 기록
                start = time.time()
            else:  # 임계값 이하 상태가 1분 지속되면 스케일 인
                end = time.time()
                if end - start >= 60.00:
                    print(f"Container가 필요 이상으로 많습니다. 현재 컨테이너 개수 : {sca}")
                    sca -= 1
                    start = 0  # 스케일 인 후 타이머 초기화
                    # docker compose scale 명령어로 컨테이너 수 조정
                    subprocess.run(["docker", "compose", "scale", f"blog={sca}"])

        # 10초 대기 후 반복
        time.sleep(10)

except KeyboardInterrupt:
    print("프로그램이 종료되었습니다.")

