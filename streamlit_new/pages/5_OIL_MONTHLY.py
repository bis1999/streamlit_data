import pandas as pd 
import streamlit as st 
import pickle


import plotly.graph_objects as go
from plotly.subplots import make_subplots

df = st.session_state["oil_data_monthly_df"]


st.title("EIA MONTHLY")

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
        tuple((all_pads_pivots.keys())))



    pivot_type = st.sidebar.radio(
        "Select Pivot Type",
        tuple((all_pads_pivots[padd].keys())))








    year_start, year_end = st.slider('Select year range', min_value=2017, max_value=2023, value=(2018, 2023))
    month_start, month_end = st.slider('Select week range', min_value=1, max_value=12, value=(1, 12))


    filtered_df = df[(df['year'] >= year_start) & (df['year'] <= year_end)]
    filtered_df = filtered_df[(filtered_df['month'] >= month_start) & (filtered_df['month'] <= month_end)]



    st.subheader("Piviots Tables for {}".format(pivot_type))
    for i in all_pads_pivots[padd][pivot_type]:
    	st.subheader(i)
    	st.dataframe(pivot_generation(filtered_df,i).round(2),width = 700)





else:
    st.title("Time Series")





    padd = st.sidebar.radio(
        "Padds",
        tuple((all_pads_pivots.keys())))



    pivot_type = st.sidebar.radio(
        "Select Pivot Type",
        tuple((all_pads_pivots[padd].keys())))

    year_start, year_end = st.slider('Select year range', min_value=2017, max_value=2023, value=(2018, 2023))
    month_start, month_end = st.slider('Select week range', min_value=1, max_value=12, value=(1, 12))


    fig = make_subplots(rows=len(all_pads_pivots[padd][pivot_type]), 
        subplot_titles = tuple(all_pads_pivots[padd][pivot_type]),cols=1, shared_xaxes=False, vertical_spacing=0.07)

# Main plot heading
    fig.update_layout(title_text=f"Time Series - {pivot_type}", title_x=0.5)

    # Loop through each item in the selected chart_type
    for idx, i in enumerate(all_pads_pivots[padd][pivot_type]):
        # Create a subplot for each item in the selected chart_type
        filtered_df = df[(df['year'] >= year_start) & (df['year'] <= year_end)]
        filtered_df = filtered_df[(filtered_df['month'] >= month_start) & (filtered_df['month'] <=  month_end )]
        filtered_df = filtered_df[filtered_df[i] != 0]

        x = filtered_df['period']
        y = filtered_df[i]

        # Add the subplot to the figure
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name=i,showlegend=False), row=idx+1, col=1)
        #fig.update_layout(title_text = i)

        #annotation_text = f"{chart_type} - {i}"
       

        # Subplot axis titles
        #fig.update_xaxes(title_text="Period", row=idx+1, col=1)
        fig.update_xaxes(title_text="period")
        fig.update_yaxes(title_text="values")


# Update the layout of the main plot
    if len(all_pads_pivots[padd][pivot_type]) <9:
        fig.update_layout(width=1000, height=2500)
    else:
        fig.update_layout(width=1000, height=6000)

    st.plotly_chart(fig)




      