import streamlit as sl
import pandas as pd
import plotly
pd.options.plotting.backend = "plotly"
# import pandas_profiling
# from streamlit_pandas_profiling import st_profile_report
import sklearn

sl.title('Dashboard MTR')
df = pd.read_csv("C:/Users/User/Desktop/Dashboards/Streamlit/navex2.csv")
sl.write(df)


options = sl.multiselect(
    'Variables',
df.keys())

col1, col2 = sl.columns(2)
with col1:
    sl.line_chart(df, x='Data', y=options)
    sl.bar_chart(df, x='Data', y=options)

with col2:
    sl.area_chart(df, x='Data', y=options)  


sl.balloons()
