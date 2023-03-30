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

# col1, col2 = st.columns(2)

def make_grid(cols,rows):
    grid = [0]*cols
    for i in range(cols):
        with st.container():
            grid[i] = st.columns(rows)
    return grid
  
mygrid = make_grid(5,3)
  
headers = df.keys()
headers = headers[2:]

# options = mygrid[0][1].multiselect(
#     'Select variables',
# headers,
# headers[0])


# Create a date slider
min_date = df['Date'].min()
max_date = df['Date'].max()
start_date, end_date = mygrid[0][0].slider("Select a date range", min_date, max_date, (min_date, max_date))

# Filter the dataset based on the date slider values
filtered_data = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]


mygrid[2][0].metric(label="Revenue (USD)", value=filtered_data['Google_Ads_Revenue_Total'].sum().round(decimals=2))
  # Plot the line chart


  
mygrid[2][1].metric(label="Spend (USD)", value=filtered_data['Google_Ads_Spend_Total'].sum().round(decimals=2))

mygrid[2][2].metric(label="Conversions", value=filtered_data['Google_Analytics_Goal_completions_Total'].sum().round(decimals=0))

mygrid[3][0].line_chart(filtered_data, x='Date', y='Google_Ads_Revenue_Total')
mygrid[3][1].line_chart(filtered_data, x='Date', y='Google_Ads_Spend_Total')
mygrid[3][2].line_chart(filtered_data, x='Date', y='Google_Analytics_Goal_completions_Total')

import plotly.express as px

fig = px.bar(filtered_data, x="Date", y=["Google_Ads_Revenue_Total", "Facebook_Ads_Revenue_Total"], title="Revenue by channel")


fig.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1
))

fig2 = px.bar(filtered_data, x="Date", y=["Google_Ads_Spend_Total", "Facebook_Ads_Spend_Total"], title="Spend by channel")

fig2.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1
))


fig3 = px.bar(filtered_data, x="Date", y=["Google_Ads_Conversions_Total", "Facebook_Ads_Conversions_Total"], title="Spend by channel")

fig3.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1
))

mygrid[4][0].plotly_chart(fig, theme="streamlit")
mygrid[4][1].plotly_chart(fig2, theme="streamlit")
mygrid[4][2].plotly_chart(fig3, theme="streamlit")
