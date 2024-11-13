# streamlit
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import subprocess
import json

import pymysql.cursors
import os

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
        choice = option_menu("Menu", ['Scale', 'Graph'],
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
        st.title("Prometheus")
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df

if __name__ == '__main__':
    main()
