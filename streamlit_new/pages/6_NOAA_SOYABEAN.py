import pandas as pd 



import pandas as pd 
import streamlit as st 
import pickle


import plotly.graph_objects as go
from plotly.subplots import make_subplots



df = pd.read_csv("NOAA_temp_data.csv")

regions = ['Chicago', 'Indiana', 'Iowa', 'Minnesota', 'Ohio']




st.title("NOAA SOYABEAN PRODUCING STATES")

page = st.sidebar.radio("Navigation", ["Pivot Tables", "Time Series Plot"])
with open('monthly_dictionary_oil.pkl', 'rb') as fp:
    all_pads_pivots = pickle.load(fp)
if page == "Pivot Tables":



    st.title("Pivot tables ")



    st.sidebar.title("Pivot Tables Options")



    def pivot_generation(df,val):
         return df.pivot_table(columns="year",values =val,index = "month",aggfunc="mean", margins=True)

    padd = st.sidebar.radio(
        "Padds",
        tuple(regions))








    year_start, year_end = st.slider('Select year range', min_value=2017, max_value=2023, value=(2018, 2023))
    month_start, month_end = st.slider('Select week range', min_value=1, max_value=12, value=(1, 12))


    filtered_df = df[(df['year'] >= year_start) & (df['year'] <= year_end)]
    filtered_df = filtered_df[(filtered_df['month'] >= month_start) & (filtered_df['month'] <= month_end)]
    filtered_df = filtered_df[filtered_df["Region"] == padd]



    st.subheader("Piviots Tables for {}".format(padd))
    for i in ['TMAX', 'TAVG', 'TMIN']:
    	st.subheader(i)
    	st.dataframe(pivot_generation(filtered_df,i).round(2),width = 700)





