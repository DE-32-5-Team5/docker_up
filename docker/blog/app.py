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

file_path = "../../data/docker_stats.csv"

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
        st.title('될까요?')

        # Prometheus 서버에 연결
        prom = PrometheusConnect(url="http://localhost:9090", disable_ssl=True)

        # 실시간 서버 사용량 쿼리 함수
        def get_cpu_usage():
            # CPU 사용량 (idle 시간을 기반으로 계산)
            query = '100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)'
            return prom.custom_query(query=query)

        def get_memory_usage():
            # 메모리 사용량
            query = '100 * (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes))'
            return prom.custom_query(query=query)

        # 데이터프레임 변환 함수
        def query_to_dataframe(metric_data, metric_name):
            # Prometheus에서 반환한 데이터를 pandas DataFrame으로 변환
            df = pd.DataFrame([
                {
                    "instance": item["metric"]["instance"],
                    metric_name: float(item["value"][1])
                } for item in metric_data
            ])
            return df

        # Streamlit 페이지 구성
        st.title("Server Usage Dashboard")
        st.subheader("Real-time CPU and Memory Usage")

        # 대시보드 업데이트
        cpu_data = get_cpu_usage()
        st.write(cpu_data)
#        memory_data = get_memory_usage()
#
#        # CPU 및 메모리 사용량 데이터프레임 생성
#        cpu_df = query_to_dataframe(cpu_data, "cpu_usage")
#        memory_df = query_to_dataframe(memory_data, "memory_usage")
#
#        # 데이터 병합
#        usage_df = pd.merge(cpu_df, memory_df, on="instance", how="inner")
#
#        # 데이터 표시
#        st.write("**CPU & Memory Usage**")
#        st.write(usage_df)
#
#        # 그래프 생성
#        fig, ax = plt.subplots(2, 1, figsize=(10, 8))
#
#        # CPU 사용량 그래프
#        ax[0].bar(usage_df['instance'], usage_df['cpu_usage'], color='skyblue')
#        ax[0].set_title("CPU Usage (%)")
#        ax[0].set_ylabel("Usage (%)")
#
#        # 메모리 사용량 그래프
#        ax[1].bar(usage_df['instance'], usage_df['memory_usage'], color='salmon')
#        ax[1].set_title("Memory Usage (%)")
#        ax[1].set_ylabel("Usage (%)")
#        ax[1].set_xlabel("Instance")
#
#        # Streamlit에 그래프 표시
#        st.pyplot(fig)
#
#        # 주기적으로 업데이트하기 위해 10초 간격으로 다시 실행
#        time.sleep(10)


if __name__ == '__main__':
    main()
