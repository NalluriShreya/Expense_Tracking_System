import streamlit as st
from datetime import datetime
import requests
import pandas as pd

API_URL = "http://localhost:8000"

def analytics_tab():   
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime(2024, 8, 1))
    with col2:
        end_date = st.date_input("End Date", datetime(2024, 8, 5))
    
    if st.button("Get Analytics"):
        payload = {
            "start_date" : start_date.strftime("%Y-%m-%d"),
            "end_date" : end_date.strftime("%Y-%m-%d")
        }
        response = requests.post(f"{API_URL}/analytics", json=payload)
        response = response.json()

        df = pd.DataFrame({
            'Category' : list(response.keys()),
            'Total' : [response[res]['total'] for res in response.keys()],
            'Percentage' : [response[res]['percentage'] for res in response.keys()]
        })

        df_sorted = df.sort_values(by='Percentage', ascending=False)

        st.title("Expense Breakdown by Category")

        st.bar_chart(df_sorted, x='Category', y='Percentage')

        st.table(df_sorted)
