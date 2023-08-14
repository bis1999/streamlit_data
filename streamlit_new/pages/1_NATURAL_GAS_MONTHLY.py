import streamlit as st
import pandas as pd 

import plotly.graph_objects as go
from plotly.subplots import make_subplots


st.title("EIA MONTHLY")

df = st.session_state["my_input"]

page = st.sidebar.radio("Navigation", ["Pivot Tables", "Time Series Plot"])

if page == "Pivot Tables":

    st.title("Pivot tables ")







    def pivot_gen(df, val, agg_='mean', idx='month', cols='year'):

        return pd.pivot_table(df, values=val, index=idx, columns=cols, aggfunc=agg_, margins=True)


    Consumption = ["Cons_Elec", "Cons_ind", "Cons_Resi", "Cons_Comm", "Cons_pipefuel", "Cons_Vehfuel", "cons_plantfuel", "Cons_tot"]
    production = ["Prod_marketed", "ext_loss", "Prod_dry", "Prod_tot"]
    Underground_Storage = ["injections", "withdrawals", "Net_withdrawals", "Tot_working", "Base_gas", "tot_storage_cap"]
    Imports_Exports = ["imp_pipe", "imp_LNG", "imp_tot", "exp_pipe", "exp_LNG", "exp_tot"]
    prices = ["pr_elec_power", "pr_LNG_exp", "pr_exp", "pr_lng_import", "pr_imp", "pr_ind", "pr_citygate", "pr_pipeexp", "pr_resi", "pr_comml"]
    temp_spot_price = ["Price_HH", "Price_k1", "Price_k2", "Price_k3"]


    dt = {
        "Production": production,
        "Consumption": Consumption,
        "Imports_Exports": Imports_Exports,
        "Underground_Storage": Underground_Storage,
        "Prices": prices,
        "Spot_price": temp_spot_price,
       
    }

       

    # Assuming you have the DataFrame 'your_dataframe' containing the data

    # Get the pivot tables

    st.sidebar.title("Pivot Tables Options")

    piv_type = st.sidebar.radio(
        "Pivot Type",
        tuple((dt.keys())))


    year_start, year_end = st.slider('Select year range', min_value=2009, max_value=2023, value=(2018, 2023))
    month_start, month_end = st.slider('Select week range', min_value=1, max_value=12 ,value=(1, 12))


    filtered_df = df[(df['year'] >= year_start) & (df['year'] <= year_end)]
    filtered_df = filtered_df[(filtered_df['month'] >= month_start) & (filtered_df['month'] <=  month_end)]



    st.subheader("Piviots Tables for {}".format(piv_type))
    for i in dt[piv_type]:
        st.subheader(i)
        st.dataframe(pivot_gen(filtered_df,i).round(2),width = 700)


else:
    st.title("Time Series")

    Consumption = ["Cons_Elec", "Cons_ind", "Cons_Resi", "Cons_Comm", "Cons_pipefuel", "Cons_Vehfuel", "cons_plantfuel", "Cons_tot"]
    production = ["Prod_marketed", "ext_loss", "Prod_dry", "Prod_tot"]
    Underground_Storage = ["injections", "withdrawals", "Net_withdrawals", "Tot_working", "Base_gas", "tot_storage_cap"]
    Imports_Exports = ["imp_pipe", "imp_LNG", "imp_tot", "exp_pipe", "exp_LNG", "exp_tot"]
    prices = ["pr_elec_power", "pr_LNG_exp", "pr_exp", "pr_lng_import", "pr_imp", "pr_ind", "pr_citygate", "pr_pipeexp", "pr_resi", "pr_comml"]
    temp_spot_price = ["Price_HH", "Price_k1", "Price_k2", "Price_k3"]


    dt = {
        "Production": production,
        "Consumption": Consumption,
        "Imports_Exports": Imports_Exports,
        "Underground_Storage": Underground_Storage,
        "Prices": prices,
        "Spot_price": temp_spot_price,
       
    }


    st.sidebar.title("Pivot Tables Options")

    chart_type = st.sidebar.radio(
        "Chart Type",
        tuple((dt.keys())))




    year_start, year_end = st.slider('Select year range', min_value=2009, max_value=2023, value=(2018, 2023))
    month_start, month_end = st.slider('Select week range', min_value=1, max_value=12 ,value=(1, 12))

    fig = make_subplots(rows=len(dt[chart_type]), 
        subplot_titles = tuple(dt[chart_type]),cols=1, shared_xaxes=False, vertical_spacing=0.05)

# Main plot heading
    fig.update_layout(title_text=f"Time Series - {chart_type}", title_x=0.5)

    # Loop through each item in the selected chart_type
    for idx, i in enumerate(dt[chart_type]):
        # Create a subplot for each item in the selected chart_type
        filtered_df = df[(df['year'] >= year_start) & (df['year'] <= year_end)]
        filtered_df = filtered_df[(filtered_df['month'] >= month_start) & (filtered_df['month'] <=  month_end)]
        filtered_df = filtered_df[filtered_df[i] != 0]

        x = filtered_df['Period']
        y = filtered_df[i]

        # Add the subplot to the figure
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name=i,showlegend=False), row=idx+1, col=1)
        fig.update_layout(title_text = i)

        #annotation_text = f"{chart_type} - {i}"
       

        # Subplot axis titles
        #fig.update_xaxes(title_text="Period", row=idx+1, col=1)
        fig.update_xaxes(title_text="Period")
        fig.update_yaxes(title_text=i)

# Update the layout of the main plot
    if len(dt[chart_type]) <9:
        fig.update_layout(width=1000, height=2500)
    else:
        fig.update_layout(width=1000, height=6000)


    


        # Subplot heading
 

    # Display the entire figure with subplots
    st.plotly_chart(fig)




  


# Your existing code

# Get the selected chart type from the user's choice


# Create subplots with shared x-axis









      