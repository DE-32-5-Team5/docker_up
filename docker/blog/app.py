# streamlit
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import pymysql.cursors
import os

# mariadb port : localhost:3551
def get_conn():
    # 여기 ip나 port나 비번이나 다 바꾸기
  conn = pymysql.connect(host=os.getenv("DB_IP","localhost"),
                            port=int(os.getenv("MY_PORT", 3551)),
                            user = 'fiveguys', password = 'five2024$',
                            database = 'parkingissue',
                            cursorclass=pymysql.cursors.DictCursor)
  return conn

def main():
    #st.set_page_config(layout="wide")
    with st.sidebar:
        choice = option_menu("Menu", ['DB', 'PLOT'],
                            icons=['bi bi-people', 'bi bi-map'],
                            menu_icon="bi bi-app-indicator", default_index=0,
                            styles={
            "container": {"padding": "4!important", "background-color": "#fafafa"},
            "icon": {"color": "black", "font-size": "25px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#fafafa"},
            "nav-link-selected": {"background-color": "#08c7b4"},
        })

    if choice == "DB":
        st.title("Testing Page")

if __name__ == '__main__':
    main()
