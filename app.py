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
# df = df.iloc[: , :5]



#----------------------------------------------------------

col1, col2, col3 = st.columns(3)
container = st.container()
  
  
headers = df.keys()
headers = headers[2:]

options = col1.container.multiselect(
    'Select variables',
headers,
headers[0])
st.text("")

# Create a date slider
min_date = df['Date'].min()
max_date = df['Date'].max()
start_date, end_date = container.slider("Select a date range", min_date, max_date, (min_date, max_date))

# Filter the dataset based on the date slider values
filtered_data = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]


revenue=st.metric(label="Revenue (USD)", value=filtered_data['Google_Ads_Revenue_Total'].sum().round(decimals=2))
  # Plot the line chart
st.line_chart(filtered_data, x='Date', y=options)


  
st.metric(label="Spend (USD)", value=filtered_data['Google_Ads_Spend_Total'].sum().round(decimals=2))
