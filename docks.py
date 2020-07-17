#!/usr/bin/env python
# coding: utf-8

# In[3]:


import json
import pandas as pd
import urllib.request
from datetime import datetime, timezone
import pytz


# In[28]:


def extract_station():
    "Extracts information regarding stations and saves to a csv and a json file"
    url_station = "https://gbfs.capitalbikeshare.com/gbfs/es/station_information.json"
    response_station = urllib.request.urlopen(url_station)
    data_station = json.loads(response_station.read())
    dic_station = {}
    i=0
    for el in data_station["data"]["stations"]:
        dic_station[i]=el
        i+=1
    df_station = pd.DataFrame.from_dict(dic_station, orient = 'index')
    station = pd.concat([df_station["station_id"],
                     df_station["name"],
                     df_station["rental_methods"],
                     df_station["lat"],
                     df_station["lon"], 
                     df_station["capacity"], 
                     df_station["region_id"],
                     df_station["station_type"]], axis=1)
    station.to_csv("Station_information.csv")
    station.to_json("Station_information.json", orient="index")
    return station.to_json(orient="index")

# In[29]:


def extract_status():
    """Extracts information regarding station status,
    converts timestamp to human readable date and saves results in a json and a csv file"""
    url_status = "https://gbfs.capitalbikeshare.com/gbfs/es/station_status.json"
    response_status = urllib.request.urlopen(url_status)
    data_status = json.loads(response_status.read())
    dic_status = {}
    i=0
    for el in data_status["data"]["stations"]:
        dic_status[i]=el
        i+=1
    df_status = pd.DataFrame.from_dict(dic_status, orient = 'index')  
    time_zone = pytz.timezone("America/Atikokan")
    timestamp_status = data_status["last_updated"]
    last_updated_status = datetime.fromtimestamp(timestamp_status).astimezone(time_zone).strftime('%Y-%m-%d %H:%M:%S')
    df_status["last_updated_date"] = datetime.fromtimestamp(timestamp_status).astimezone(time_zone).strftime("%Y-%m-%d %H:%M:%S")
    status = pd.concat([df_status["station_id"],
                    df_status["num_bikes_available"],
                    df_status["num_docks_available"], 
                    df_status["num_ebikes_available"], 
                    df_status["num_bikes_disabled"],
                    df_status["num_docks_disabled"], 
                    df_status["last_reported"],
                    df_status["is_renting"], 
                    df_status["is_returning"],
                    df_status["last_updated_date"]], axis=1)
    status.to_csv("Station_status.csv")
    status.to_json("Station_status.json", orient="index")
    return status.to_json(orient="index")


# In[58]:


def join_info():
    "Joins data regarding informations on stations with data regarding their status. Produces a csv and a json."
    extract_station()
    extract_status()
    status=pd.read_csv("Station_status.csv")
    status.drop(columns=["Unnamed: 0"])
    stations=pd.read_csv("Station_information.csv")
    stations.drop(columns=["Unnamed: 0"])
    station_status = status.set_index("station_id").join(stations.set_index("station_id"), on=['station_id'], how='right' , lsuffix='_left', rsuffix='_right')
    station_status = station_status.rename(columns={'name': 'Station_Name'})
    station_status["num_bikes_available"] = station_status["num_bikes_available"] - station_status["num_bikes_disabled"]
    station_status["num_docks_available"] = station_status["num_docks_available"] - station_status["num_docks_disabled"]
    station_status = station_status.drop(['num_bikes_disabled', 'num_docks_disabled'], axis=1)
    quick_look = pd.concat([station_status["Station_Name"],
                             station_status["num_bikes_available"],
                             station_status["num_docks_available"],
                             station_status["num_ebikes_available"],
                             station_status["capacity"],
                             station_status["lat"],
                             station_status["lon"],
                             station_status["last_updated_date"]], axis=1)
    quick_look = quick_look.rename(columns={'lat': 'station_lat',
                                         'lon': 'station_lon'})
    quick_look.to_csv("Stat_complete_info.csv")
    quick_look.to_json("Stat_complete_info.json",orient="index")
    return quick_look.to_json(orient="index")

def join_info_mask():
    pyobj = json.loads(join_info())

    docks_final = {"docks":[]}

    for key, value in pyobj.items():
        docks_final["docks"].append(value)

    return docks_final


