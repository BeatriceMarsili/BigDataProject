#!/usr/bin/env python
# coding: utf-8



import json
import pandas as pd
import urllib.request
from datetime import datetime, timezone
import pytz




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
    return "Produced a csv and a json file with information regarding stations."


# In[83]:


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
    return "Produced a csv and a json file with stations and their current status."

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
    station_status["avlb_bikes"] = station_status.num_bikes_available.apply(lambda x: True if x > 2 else False)
    station_status["avlb_docks"] = station_status.num_docks_available.apply(lambda x: True if x >2 else False)
    quick_look = pd.concat([station_status["Station_Name"],
                             station_status["num_bikes_available"],
                             station_status["num_docks_available"],
                             station_status["num_ebikes_available"],
                             station_status["capacity"],
                             station_status["lat"],
                             station_status["lon"],
                             station_status["last_updated_date"],
                             station_status["avlb_bikes"],
                             station_status["avlb_docks"]], axis=1)
    quick_look = quick_look.rename(columns={'lat': 'station_lat',
                                         'lon': 'station_lon'})
    quick_look.to_csv("Stat_complete_info.csv")
    quick_look.to_json("Stat_complete_info.json", orient="index")
    return "Produced a csv and a json file with joined information abouth stations and their status"


mus = pd.read_csv("museums_info.csv")
closed = list(mus.loc[(mus["museums/permanently_closed"] == True), "museums/name"])

df= pd.read_csv("Museums_in_DC.csv", sep=";")
df = df[-df.NAME.isin(closed)]
df.to_csv("Musuems_in_DC_filt.csv")




mus = pd.read_csv("mus_close_stat.csv")
info = pd.read_csv("Stat_complete_info.csv")
final = pd.merge(final, info, on='station_id')
final.drop(columns=["Station_Name"])
final = mus.groupby(["museum"]).head(5)
final.reset_index(drop=True, inplace=True)
final.to_csv("mus_close_stat_filt.csv")




stat = pd.read_csv("stat_close_mus.csv")
final = stat.groupby(["name"]).head(5)
final = pd.merge(final, info, on='station_id')
final.drop(columns=["Station_Name"])
final.reset_index(drop=True, inplace=True)
final.to_csv("stat_close_mus_filt.csv")






