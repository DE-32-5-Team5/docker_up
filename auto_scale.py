import subprocess
import json
import time
import yaml
import csv
import os

# 스케일링 조건을 위한 설정
start = 0  # 타이머 초기화
#sca = 1  # 현재 컨테이너 개수
#lim = 1  # CPU 임계값 설정 (예시로 5%로 설정)

# yml 파일을 읽어서 임계값 가져오기
with open('docker-compose.yml') as f:
    file = yaml.full_load(f)
lim = float(file['services']['parking']['deploy']['resources']['limits']['cpus'])


# 현재 스크립트 위치를 기준으로 CSV 파일 경로 설정
csv_dir = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(csv_dir, exist_ok=True)  # 디렉토리가 없으면 생성
csv_file = os.path.join(csv_dir, 'docker_stats.csv')  # 상대 경로로 CSV 파일 지정


# CSV 파일이 없을 때만 헤더를 추가
if not os.path.exists(csv_file):
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Container', 'Name', 'CPU %', 'Memory Usage','Sclae'])



try:
    while True:
        scale_done = "NO"
        
        # docker stats 명령어 실행 및 oneshot-parking 관련 컨테이너 수 확인
        len_result = subprocess.run(
            'docker stats  --no-stream | grep "oneshot-parking"',
            capture_output=True, text=True, shell=True
        )

        # 결과를 줄 단위로 나누기
        sca = len(len_result.stdout.strip().splitlines())


        # Docker stats를 통해 특정 컨테이너의 CPU 사용량 가져오기
        r = subprocess.run(
            ["docker", "stats", "oneshot-parking-1", "--no-stream", "--format", "{{ json .}}"],
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
                    scale_done = "Up"
                    sca += 1
                    subprocess.run(["docker", "compose", "scale", f"parking={sca}"])
                    print(f"Container가 임계값을 넘은지 1분이 지났습니다. 현재 컨테이너 개수 : {sca}")
                    start = 0  # 스케일 아웃 후 타이머 초기화
                    # docker compose scale 명령어로 컨테이너 수 조정
                    

        # 스케일 인 조건: CPU 사용률이 임계값 이하이고, 컨테이너가 2개 이상일 때
        elif per <= lim and sca > 1:
            if not start:  # 처음 조건을 만족한 경우, 시작 시간 기록
                start = time.time()
            else:  # 임계값 이하 상태가 1분 지속되면 스케일 인
                end = time.time()
                if end - start >= 60.00:
                    scale_done = "Down"
                    sca -= 1
                    start = 0  # 스케일 인 후 타이머 초기화
                    # docker compose scale 명령어로 컨테이너 수 조정
                    subprocess.run(["docker", "compose", "scale", f"parking={sca}"])
                    print(f"Container가 필요 이상으로 많습니다. 현재 컨테이너 개수 : {sca}")


        result = subprocess.run(
            'docker stats --no-stream --format "table {{.Container}},{{.Name}},{{.CPUPerc}},{{.MemUsage}}" | grep "oneshot-parking-1"',
            capture_output=True, text=True, shell=True
        )

         # 출력 결과를 줄 단위로 분리하고 CSV 파일에 저장
        line = result.stdout
        line =  f"{line.strip()} , {scale_done}"
        
        with open(csv_file, 'a', newline='') as f:
            writer = csv.writer(f)
            data = line.split(',')
            writer.writerow(data)
            print(f"데이터 저장: {data}")

        # 10초 대기 후 반복
        time.sleep(10)

except KeyboardInterrupt:
    print("프로그램이 종료되었습니다.")

