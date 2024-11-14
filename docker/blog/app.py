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
import time
from datetime import datetime
import requests

from prometheus_api_client import PrometheusConnect

file_path = "/home/kimpass189/last_dance/docker_up/data/docker_stats.csv"
url = "http://localhost:8013/metrics"

def fetch_cpu_usage():
    try:
        response = requests.get(url)
        metrics = response.text
        for line in metrics.splitlines():
            if line.startswith("process_cpu_seconds_total"):
                cpu_usage = float(line.split()[-1])
                return cpu_usage
    except Exception as e:
        st.error(f"Failed to fetch metrics: {e}")
    return None

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
        st.title("Real-Time CPU Usage Dashboard")

        # Initialize or load previous data
        if "cpu_usage_data" not in st.session_state:
            st.session_state.cpu_usage_data = []
            st.session_state.timestamps = []

        # Fetch new CPU usage data
        cpu_usage = fetch_cpu_usage()
        if cpu_usage is not None:
            st.session_state.cpu_usage_data.append(cpu_usage)
            st.session_state.timestamps.append(datetime.now())

        # Ensure lists are of the same length before creating the DataFrame
        if len(st.session_state.cpu_usage_data) == len(st.session_state.timestamps):
            # Create a DataFrame for plotting
            df = pd.DataFrame({
                'Time': st.session_state.timestamps,
                'CPU Usage': st.session_state.cpu_usage_data
            })

            # Plotting
            plt.figure(figsize=(10, 5))
            plt.plot(df['Time'], df['CPU Usage'], label="CPU Usage (seconds)")
            plt.xlabel("Time")
            plt.ylabel("CPU Usage (seconds)")
            plt.title("CPU Usage Over Time")
            plt.legend()
            st.pyplot(plt)

        # Set refresh interval to 1 minute
        time.sleep(60)
        st.experimental_rerun()  # Refreshes the Streamlit app to get new data
if __name__ == '__main__':
    main()
