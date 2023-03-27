# streamlit_app.py

import streamlit as st
from google.oauth2 import service_account
from gsheetsdb import connect
import pandas as pd

st.set_page_config(page_title = 'Streamlit Demo Dashboard',
                    layout='wide',
                    initial_sidebar_state='collapsed')

# Create a connection object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)
conn = connect(credentials=credentials)

# Perform SQL query on the Google Sheet.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
# @st.cache(ttl=600)
def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows

sheet_url = st.secrets["private_gsheets_url"]
rows = run_query(f'SELECT * FROM "{sheet_url}"')

st.title("Streamlit Demo Dashboard")

# # Print results.
# for row in rows:
df = pd.DataFrame(data=rows)
df

options = st.multiselect(
    'Select variables',
df.keys())

import datetime
st.title("Date range")

start_date, end_date = st.select_slider(
    'Select a date range',
    options=df['Year_and_month'],
    value=('2021|01', '2022|12'))



st.line_chart(df, x='Year_and_month', y='Facebook_Ads_Spend_Total')
