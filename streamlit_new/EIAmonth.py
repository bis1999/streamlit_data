import pandas as pd 
import numpy as np
import requests
from pandas import json_normalize
import pickle
from datetime import date
from stqdm import stqdm


global inserting_api



inserting_api = "?api_key=15RJrfyJLw5Zg2uLi07Erq4VholSJuP3Dptyl8vK&"



def replace_char(string, char_to_replace, new_string):
    result = ""
    for char in string:
        if char == char_to_replace:
            result += new_string
        else:
            result += char
    return result



def generate_csv(url,save = False,Head_cat=None,sub_cat = None,return_ = True):
    url_with_api = replace_char(url,"?",inserting_api)
    r = requests.get(url_with_api)
    json_data = r.json()
    df = json_normalize(json_data["response"]["data"])
    if save == True:
        df.to_csv("Series/{}_{}.csv".format(Head_cat,sub_cat))
    
    if return_ == True:
        return df
    

def return_csv():
    with open("all_apis", "rb") as fp:   # Unpickling
           all_urls = pickle.load(fp)
            
    dtsets = []
    for i in stqdm(all_urls):
        a = generate_csv(i)
        dtsets.append(a)
    df = pd.concat(dtsets)
    
    final_ = df.pivot_table(index = "period",columns="process-name", values="value")
    final_ = final_[final_.index > '1999-12']
    return final_
        

    
import calendar

def get_days_in_month(row):
    month = row['month']
    year = row['year']
    if month < 1 or month > 12:
        return "Invalid month. Month should be between 1 and 12."
    num_days = calendar.monthrange(year, month)[1]
    return num_days



def scaling_and_renaming():
    data= return_csv()
    df_aux = pd.DataFrame()
    df_aux["Period"] = data.index
    df_aux["month"] = pd.DatetimeIndex(df_aux['Period']).month  
    df_aux["year"] = pd.DatetimeIndex(df_aux['Period']).year  
    df_aux['days_in_month'] = df_aux.apply(get_days_in_month, axis=1)
    
    conversions = pd.read_csv("Final_conversions.csv")

    conversions_dict = dict(zip(conversions["Variable "],conversions["Conversion"]))
    
   
    for i in list(conversions_dict.keys()):
        if conversions_dict[i] == 'a':
            df_aux[i]= list(data[i]/1000)
        elif conversions_dict[i] == 'b':
            df_aux[i]= list(data[i]/1000)
            df_aux[i] = list(df_aux[i]/df_aux["days_in_month"])
        else:
             df_aux[i]= list(data[i])
    df_aux =  df_aux.fillna(0).round(2)
    a = pd.read_csv("col_names.csv")
    cols_con = dict(zip(a["Current col name"],a["Suggested col_name"]))
    df_aux = df_aux.rename(columns=cols_con)
    today = date.today()

    df_aux.to_csv("Data/{}.csv".format(str(today)))
   
    return df_aux

                
    
