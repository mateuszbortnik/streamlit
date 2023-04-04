# streamlit_app.py

import streamlit as st
from google.oauth2 import service_account
from gsheetsdb import connect
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
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
  
mygrid = make_grid(7,3)
  
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

# fig = px.bar(filtered_data, x="Date", y=["Google_Ads_Revenue_Total", "Facebook_Ads_Revenue_Total"], title="Revenue by channel")


# fig.update_layout(legend=dict(
#     orientation="h",
#     yanchor="bottom",
#     y=1.02,
#     xanchor="right",
#     x=1
# ))

# fig2 = px.bar(filtered_data, x="Date", y=["Google_Ads_Spend_Total", "Facebook_Ads_Spend_Total"], title="Spend by channel")

# fig2.update_layout(legend=dict(
#     orientation="h",
#     yanchor="bottom",
#     y=1.02,
#     xanchor="right",
#     x=1
# ))


# fig3 = px.bar(filtered_data, x="Date", y=["Google_Ads_Conversions_Total", "Facebook_Ads_Conversions_Total"], title="Conversions by channel")

# fig3.update_layout(legend=dict(
#     orientation="h",
#     yanchor="bottom",
#     y=1.02,
#     xanchor="right",
#     x=1
# ))

mygrid[4][0].bar_chart(data=filtered_data, x="Year_and_month", y=["Google_Ads_Revenue_Total", "Facebook_Ads_Revenue_Total"], use_container_width=True)
mygrid[4][1].bar_chart(data=filtered_data, x="Year_and_month", y=["Google_Ads_Spend_Total", "Facebook_Ads_Spend_Total"], use_container_width=True)
mygrid[4][2].bar_chart(data=filtered_data, x="Year_and_month", y=["Google_Ads_Conversions_Total", "Facebook_Ads_Conversions_Total"], use_container_width=True)



# df_corr = filtered_data.iloc[: , :10].corr()
# df_corr

# fig4 = go.Figure()
# fig4.add_trace(
#     go.Heatmap(
#         x = df_corr.columns,
#         y = df_corr.index,
#         z = np.array(df_corr)
#     )
# )

# st.plotly_chart(fig4, theme="streamlit")

# fig4, ax = plt.subplots()
# sns.heatmap(filtered_data.corr(), ax=ax)
# st.write(fig4)

xaxis = mygrid[5][0].selectbox(
    'Select spend channel',
    ('Facebook_Ads_Spend_Total', 'Facebook_Ads_Spend_Prospecting', 'Facebook_Ads_Spend_Remarketing_Brand_Nurturing', 'Facebook_Ads_Spend_not_set', 'Google_Ads_Spend_Total', 'Google_Ads_Spend_Prospecting', 'Google_Ads_Spend_Remarketing_Brand_Nurturing', 'Google_Ads_Spend_not_set'))

yaxis = mygrid[5][0].selectbox(
    'Select spend channel',
    ('Facebook_Ads_Revenue_Total', 'Facebook_Ads_Revenue_Prospecting', 'Facebook_Ads_Revenue_Remarketing_Brand_Nurturing', 'Facebook_Ads_Revenue_not_set', 'Google_Ads_Revenue_Total', 'Google_Ads_Revenue_Prospecting', 'Google_Ads_Revenue_Remarketing_Brand_Nurturing', 'Google_Ads_Revenue_not_set'))


ac = alt.Chart(filtered_data).mark_circle(size=60).encode(
    x=xaxis,
    y=yaxis,
#     color='Origin',
    tooltip=['Year_and_month',xaxis, yaxis]
).interactive()
mygrid[5][1].altair_chart(ac, use_container_width=True, theme="streamlit")

mygrid[5][3].metric(filtered_data[xaxis].corr(filtered_data[yaxis]))
