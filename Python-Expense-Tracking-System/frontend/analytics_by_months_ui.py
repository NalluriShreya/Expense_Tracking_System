import streamlit as st
from datetime import datetime
import requests
import pandas as pd
import calendar

API_URL = "http://localhost:8000"

def analytics_by_months_tab(): 
    response = requests.get(f"{API_URL}/expenses/analytics/month")
    response = response.json()

    df = pd.DataFrame({
        "Month": [calendar.month_name[data["Month"]] for data in response],
        "Expenses": [data["Expenses"] for data in response]
    })


    st.header("Expense Breakdown by Months")

    st.bar_chart(df, x="Month", y="Expenses")

    df["Expenses"] = df["Expenses"].apply(lambda x: f"{x:.2f}")
    st.table(df)