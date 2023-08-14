import streamlit as st
import pandas as pd
from EIAmonth import scaling_and_renaming
from datetime import date
import plotly.graph_objects as go
import glob
import os
from tqdm import tqdm 
from Oil_dowload import generate_csv
from stqdm import stqdm
import pickle
from Week_Underground import get_weekly_data
import base64

import streamlit as st



def download_link(df, filename, text):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # Encode to base64
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href


st.set_page_config(
    page_title="Commodity Analysis",
    page_icon="📊"
)

st.title("Data Update Page")
st.sidebar.success("Select a page above.")





# Using Markdown to change text color

## EIA MONTHLY


st.subheader(':green[EIA Gas Monthly]')
datasets = glob.glob('Data/*.csv')
dates = [i.split(".")[0].split("/")[1] for i in datasets]
data_ = max(dates)

st.write("Last Updated EIA Gas monthly: {} ".format(data_ ))
st.write("Data Source : https://www.eia.gov/dnav/ng/ng_sum_lsum_dcu_nus_m.htm")
if st.button("Update EIA Gas monthly"):
        # Call the function to update the dataset
        df = scaling_and_renaming()# # Reload the updated dataset
        today = date.today()
        df.to_csv('Data/{}.csv'.format(str(today)))
        st.write("Natural Gas Monthly Data Updated on {}".format(str(today)))


      
        
else:
    
    df = pd.read_csv("Data/{}.csv".format(data_))
st.session_state["my_input"] = df






tmp_download_link = download_link(df, 'EIA_GAS_MONTHLY.csv', 'Click here to download your data!')
st.markdown(tmp_download_link, unsafe_allow_html=True)



## Oil 
st.subheader(':green[EIA Oil Weekly]')
datasets = glob.glob('Data_oil/*.csv')
dates = [i.split(".")[0].split("/")[1] for i in datasets]
data_ = max(dates)

st.write("Last Updated EIA OIL Weekly: {} ".format(data_ ))
st.write("Data Source : https://www.eia.gov/dnav/pet/pet_sum_sndw_dcus_nus_w.htm")

if st.button("Update EIA Oil Weekly"):
    with open('oil_2015.pkl', 'rb') as f:
       oils_urls = pickle.load(f)

    df = []
    for i in stqdm(oils_urls):
        a = generate_csv(i)
        df.append(a)
    comdt = pd.concat(df)
    oil_data= pd.pivot_table(data = comdt,values="value",columns="series-description",index = "period")
    oil_data = oil_data.reset_index()
    oil_data["period"] = pd.DatetimeIndex(oil_data["period"])
    oil_data["week"] = oil_data["period"].dt.isocalendar().week
    oil_data["year"] =  oil_data["period"].dt.isocalendar().year
    today = date.today()
    oil_data.to_csv('Data_oil/{}.csv'.format(str(today)))
    st.write("Natural Oil Weekly on {}".format(str(today)))
else:
    oil_data = pd.read_csv("Data_oil/{}.csv".format(data_))


st.session_state["oil"] = oil_data

tmp_download_link = download_link(oil_data, 'OIL_WEEKLY.csv', 'Click here to download your data!')
st.markdown(tmp_download_link, unsafe_allow_html=True)





st.subheader(':green[EIA Gas Weekly]')
datasets = glob.glob('dataweek/*.csv')
dates_week = [i.split(".")[0].split("/")[1] for i in datasets]
data_Week = max(dates_week)

st.write("Last Updated EIA GAS Weekly: {} ".format(data_Week))
st.write("Data Source : :red[https://www.eia.gov/dnav/ng/ng_stor_wkly_s1_w.htm]")

if st.button("Update EIA GAS Weekly"):

    data_weekly_gas = get_weekly_data()
    today = date.today()
    data_weekly_gas.to_csv('dataweek/{}.csv'.format(str(today)))
    st.write("Natural Gas Weekly on {}".format(str(today)))
else:
    data_weekly_gas = pd.read_csv("dataweek/{}.csv".format(data_Week))



tmp_download_link = download_link(data_weekly_gas, 'GAS_WEEKLY.csv', 'Click here to download your data!')
st.markdown(tmp_download_link, unsafe_allow_html=True)



st.session_state["data_weekly_gas"] =  data_weekly_gas


st.subheader(':green[NOAA CDD/HDD]')
st.write("Data Source: https://ftp.cpc.ncep.noaa.gov/htdocs/products/analysis_monitoring/cdus/degree_days/archives/")

noaa_datasets = glob.glob('noaa/*.csv')
noaa_week = [i.split(".")[0].split("/")[1] for i in noaa_datasets]
noaa_date = max(noaa_week)

st.write("Last NOAA: {} ".format(noaa_date))
st.write("https://www.eia.gov/dnav/ng/ng_stor_wkly_s1_w.htm")

if st.button("Update NOAA"):
    noaa_ = pd.read_csv("noaa/{}.csv".format(noaa_date))

    today = date.today()
    st.write("NOAA on {}".format(str(today)))
else:
    noaa_ = pd.read_csv("noaa/{}.csv".format(noaa_date))


st.session_state["noaa_df"] =  noaa_

tmp_download_link = download_link(noaa_, 'NOAA.csv', 'Click here to download your data!')
st.markdown(tmp_download_link, unsafe_allow_html=True)





    
st.subheader(':green[Oil Monthly]')
st.write("Data Source: https://ftp.cpc.ncep.noaa.gov/htdocs/products/analysis_monitoring/cdus/degree_days/archives/")

if st.button("Update EIA OIL MONTHLY"):
    
    with open('monthly_oil_apis.pkl', 'rb') as f:
       oils_urls = pickle.load(f)

    df = []
    for i in stqdm(oils_urls):
        a = generate_csv(i)
        df.append(a)
    comdt = pd.concat(df)
    oil_data= pd.pivot_table(data = comdt,values="value",columns="series-description",index = "period")
    oil_data = oil_data.reset_index()
    oil_data["period"] = pd.DatetimeIndex(oil_data["period"])
    oil_data["month"] = oil_data["period"].dt.month
    oil_data["year"] =  oil_data["period"].dt.year
    today = date.today()
    oil_data.to_csv('Data_montly_oil/{}.csv'.format(str(today)))
   #st.write("Natural Oil Weekly on {}".format(str(today)))

    #today = date.today()
    #st.write("NOAA on {}".format(str(today)))
else:
    oil_data_monthly = pd.read_csv("Monthly_oil_data.csv")


st.session_state["oil_data_monthly_df"] =  oil_data_monthly

tmp_download_link = download_link(oil_data_monthly, 'OIL_MONTHLY.csv', 'Click here to download your data!')
st.markdown(tmp_download_link, unsafe_allow_html=True)

