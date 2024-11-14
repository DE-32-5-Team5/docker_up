# streamlit
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import matplotlib.pyplot as plt
import subprocess
import json
import numpy as np

import pymysql.cursors
import os
from datetime import datetime
import requests

from prometheus_api_client import PrometheusConnect

# mariadb port : localhost:3551
#def get_conn():
#    # 여기 ip나 port나 비번이나 다 바꾸기
#  conn = pymysql.connect(host=os.getenv("DB_IP","localhost"),
#                            port=int(os.getenv("MY_PORT", 3551)),
#                            user = 'fiveguys', password = 'five2024$',
#                            database = 'parkingissue',
#                            cursorclass=pymysql.cursors.DictCursor)
#  return conn
def get_cpu_usage():
    # Prometheus 쿼리: CPU 사용량 (사용된 CPU 시간 비율)
    query = 'rate(node_cpu_seconds_total{mode="idle"}[1m])'
    result = prom.custom_query(query)

    # 쿼리 결과를 Pandas DataFrame으로 변환
    cpu_usage = []
    for data in result:
        timestamp = datetime.utcfromtimestamp(int(data['value'][0]))  # Unix 타임스탬프를 datetime으로 변환
        value = 100 - float(data['value'][1])  # 'idle' 상태가 아닌 CPU 사용량
        cpu_usage.append([timestamp, value])

    # DataFrame으로 변환
    df = pd.DataFrame(cpu_usage, columns=['Timestamp', 'CPU Usage (%)'])
    return df

file_path = "../../data/docker_stats.csv"
prom = PrometheusConnect(url="http://localhost:9090", disable_ssl=True)

def main():
    #st.set_page_config(layout="wide")
    with st.sidebar:
        choice = option_menu("Menu", ['Scale', 'Graph','test'],
                            icons=['bi bi-people', 'bi bi-map'],
                            menu_icon="bi bi-app-indicator", default_index=0,
                            styles={
            "container": {"padding": "4!important", "background-color": "#fafafa"},
            "icon": {"color": "black", "font-size": "25px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#fafafa"},
            "nav-link-selected": {"background-color": "#08c7b4"},
        })

    if choice == "Scale":
        st.title("수동 스케일링 관리 페이지")
        # 수동 스케일 버튼 활성화
        # 컨테이너 개수 수동 조정해서 원하는 만큼 스케일링 하도록
        if st.button('CPU 사용량 조회', type="primary"):
            r=subprocess.run(["docker","stats","oneshot-parking-1","--no-stream","--format","{{ json .}}"],
                capture_output=True, text=True)
        # {"BlockIO":"0B / 0B","CPUPerc":"0.01%","Container":"samdul-blog-1","ID":"710c301a218e","MemPerc":"0.32%","MemUsage":"24.51MiB / 7.543GiB","Name":"samdul-blog-1","NetIO":"1.32kB / 0B","PIDs":"82"}
            j = json.loads(r.stdout)
            per = float(j["CPUPerc"][:-1])
        
            st.subheader(f'현재 CPU 사용량은 {per}% 입니다.')

        scale_num = st.number_input("스케일링할 컨테이너 개수", min_value = 1, value= "min", key = "input1")
        if st.button('Container Scale', type = "primary"):
            subprocess.run(["docker", "compose", "scale", f"parking={scale_num}"])
            st.subheader(f'스케일링 완료, 컨테이너 개수 : {scale_num}')
    elif choice == "Graph":
        st.title("DashBoard")
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df['CPU %'] = df['CPU %'].apply(lambda x: float(x[:-2]))
            df
            # 시각화
            df_up = df[df['Sclae'] == ' Up']
            df_down = df[df['Sclae'] == ' Down']

            plt.plot(df.index, df['CPU %'])
            plt.scatter(df_up.index, df_up['CPU %'], color = 'r', label = "Scale Up")
            plt.scatter(df_down.index, df_down['CPU %'], color = 'b', label = "Scale Down")
            plt.title('Scale Graph')
            plt.xticks(df.index, fontsize = 8)
            plt.legend()
            st.pyplot(plt)
        else:
            st.header("파일이 없습니다😣")
            st.text(f"파일 저장 위치 : {file_path}")
    else:
        st.title("CPU Usage Dashboard")


if __name__ == '__main__':
    main()
