import streamlit as st
import duckdb
import sys
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import DB_PATH


st.set_page_config(page_title="Budget Dashboard", layout="wide")

con = duckdb.connect(str(DB_PATH), read_only=True)

page = st.sidebar.radio("Navigate", ["Monthly Overview", "Transactions", "Trends"])

if page == "Monthly Overview":
    st.title("Monthly Overview")
    
    df = con.sql("""
        SELECT transaction_month, monthly_income, monthly_expenses
        FROM main_marts.fct_budget_vs_actual
        ORDER BY transaction_month
    """).df()
    
    st.dataframe(df)
    st.bar_chart(df.set_index("transaction_month"))


elif page == "Transactions":
    st.title("Transactions")
    # query raw.transactions here

elif page == "Trends":
    st.title("Trends")
    # query fct_monthly_spending here
