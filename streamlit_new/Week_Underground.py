
import numpy as np 

import pandas as pd 
import requests
from pandas import json_normalize
import pickle
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

    

        
work_gas_week = {}

work_gas_week["total_lower_48"] = "https://api.eia.gov/v2/natural-gas/stor/wkly/data/?frequency=weekly&data[0]=value&facets[series][]=NW2_EPG0_SWO_R48_BCF&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000"

work_gas_week["east"] = "https://api.eia.gov/v2/natural-gas/stor/wkly/data/?frequency=weekly&data[0]=value&facets[series][]=NW2_EPG0_SWO_R31_BCF&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000"

work_gas_week["midwest"] = "https://api.eia.gov/v2/natural-gas/stor/wkly/data/?frequency=weekly&data[0]=value&facets[series][]=NW2_EPG0_SWO_R32_BCF&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000"

work_gas_week["Mountain"]="https://api.eia.gov/v2/natural-gas/stor/wkly/data/?frequency=weekly&data[0]=value&facets[series][]=NW2_EPG0_SWO_R34_BCF&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000"
work_gas_week["Pacific"] = "https://api.eia.gov/v2/natural-gas/stor/wkly/data/?frequency=weekly&data[0]=value&facets[series][]=NW2_EPG0_SWO_R35_BCF&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000"
work_gas_week["South_central"] = "https://api.eia.gov/v2/natural-gas/stor/wkly/data/?frequency=weekly&data[0]=value&facets[series][]=NW2_EPG0_SWO_R33_BCF&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000"

work_gas_week["Salt"]  = "https://api.eia.gov/v2/natural-gas/stor/wkly/data/?frequency=weekly&data[0]=value&facets[series][]=NW2_EPG0_SSO_R33_BCF&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000"

work_gas_week["Nonsalt"] = "https://api.eia.gov/v2/natural-gas/stor/wkly/data/?frequency=weekly&data[0]=value&facets[series][]=NW2_EPG0_SNO_R33_BCF&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000"



def get_weekly_data():
    all_urls = work_gas_week.values()

    dfs = [] 
    for i in all_urls:
        a = generate_csv(i)
        dfs.append(a)
    df = pd.concat(dfs)
        
        
    final_ = df.pivot_table(index = "period",columns="series-description", values="value")
    new_cols = ["East","Lower_48",'Midwest',"Mountain","Nonsalt","Pacific","Salt","South central"]
    cols_dict = dict(zip(list(final_.columns),new_cols))
    final_ = final_.rename(columns=cols_dict)
    final_["Period"] = final_.index
    final_["Period"] = pd.DatetimeIndex(final_["Period"])

    final_["Week"] = final_["Period"].dt.isocalendar().week
    final_["Year"] = final_["Period"].dt.isocalendar().year

   

  
    
    return final_


