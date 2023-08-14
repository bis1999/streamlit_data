




import plotly.express as px




import streamlit as st
import pandas as pd 

import plotly.graph_objects as go
from plotly.subplots import make_subplots


st.title("NOAA")
df = st.session_state["noaa_df"]

page = st.sidebar.radio("Navigation", ["Pivot Tables", "Time Series Plot"])

if page == "Pivot Tables":

    st.title("Pivot tables ")







    def pivot_gen(df, val, agg_='sum', idx='month', cols='year'):

        return pd.pivot_table(df, values=val, index=idx, columns=cols, aggfunc=agg_, margins=True)



       

    # Assuming you have the DataFrame 'your_dataframe' containing the data

    # Get the pivot tables

    st.sidebar.title("Pivot Tables Options")

    piv_type = st.sidebar.radio(
        "Pivot Type",
        tuple( [ 'wcdd', 'wcdd_dev', 'hdd', 'hdd_dev'])
)

    year_start, year_end = st.slider('Select year range', min_value=2009, max_value=2023, value=(2018, 2023))
    week_start, week_end = st.slider('Select week range', min_value=1, max_value=12 ,value=(1, 12))


    filtered_df = df[(df['year'] >= year_start) & (df['year'] <= year_end)]
    filtered_df = filtered_df[(filtered_df['month'] >= week_start) & (filtered_df['month'] <=  week_end)]



    st.subheader("Piviots Tables for {}".format(piv_type))
       
    st.dataframe(pivot_gen(filtered_df,piv_type).round(2),width = 1000)


else:

    st.title("Time Series")
    st.sidebar.title("Time Series Options")
    piv_type = st.sidebar.radio(
	        "Pivot Type",
	        tuple( [ 'wcdd', 'wcdd_dev', 'hdd', 'hdd_dev']))
    year_start, year_end = st.slider('Select year range', min_value=2009, max_value=2023, value=(2018, 2023))
    week_start, week_end = st.slider('Select week range', min_value=1, max_value=12 ,value=(1, 12))
    filtered_df = df[(df['year'] >= year_start) & (df['year'] <= year_end)]
    filtered_df = filtered_df[(filtered_df['month'] >= week_start) & (filtered_df['month'] <=  week_end)]
    fig = px.line(filtered_df, x="Period", y=piv_type, title = "Time Series Plot of {}".format(piv_type))

    st.plotly_chart(fig)
	

    

    




	

    
    


    

	
  


# Your existing code

# Get the selected chart type from the user's choice


# Create subplots with shared x-axis









