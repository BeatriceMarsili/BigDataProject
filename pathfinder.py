#!/usr/bin/env python
# coding: utf-8

# In[16]:


import pandas as pd
import numpy as np
import geopy.distance 
import json

import urllib.request
from numpy.random import randint
# In[17]:

def generate_distances_filter():
    mus = pd.read_csv("museums_info.csv")
    closed = list(mus.loc[(mus["museums/permanently_closed"] == True), "museums/name"])

    musemus_dc_csv_url = "https://opendata.arcgis.com/datasets/2e65fc16edc3481989d2cc17e6f8c533_54.csv"
    musemus_dc_csv_response = urllib.request.urlopen(musemus_dc_csv_url)
    df = pd.read_table(musemus_dc_csv_response, sep=",")
    df = df[-df.NAME.isin(closed)]
    df.to_csv("dcmus_filtered.csv")
    print(mus.shape, df.shape)

    # In[89]:
    mus = pd.read_csv("mus_close_stat.csv")
    final = mus.groupby(["museum"]).head(5)
    final.reset_index(drop=True, inplace=True)
    final.to_csv("mus_close_stat_filtered.csv")

    # In[90]:
    stat = pd.read_csv("stat_close_mus.csv")
    final = stat.groupby(["name"]).head(5)
    final.reset_index(drop=True, inplace=True)
    final.to_csv("stat_close_mus_filtered.csv")

def random_pos_wash():
    #"Returns a random point on Washington territory"
    lon=randint(-77087171, -76971923, 1)
    lat=randint(38857369 ,38938736, 1)
    return lon[0]/1000000, lat[0]/1000000


# In[57]:


def user_path(lat, lon, count):
    #"Given longitude and latitude returns a list of 6 museums and related stations"
    generate_distances_filter()

    stat=pd.read_csv("stat_close_mus_filtered.csv")
    stat = stat.drop('Unnamed: 0', 1)
    stat_point = list(zip(stat.lon, stat.lat))
    current= np.inf
    path= {}
    top_stat = {}
    for el in stat_point:
        dist = geopy.distance.distance((lon, lat), el).miles
        if current > dist:
            current=dist 
            top_stat = stat.loc[(stat['lat'] == el[1]) & (stat["lon"]==el[0])]
    path["1_station"]=[(list(top_stat["lon"])[0], list(top_stat["lat"])[0]), list(top_stat["name"])[0]]
   
    if list(top_stat["region_id"])[0]==42.0:
        I_mus = stat.loc[(stat["name"]==list(top_stat["name"])[0])].tail(1)
        path["1_museum"]=[(list(I_mus["longitude"])[0], list(I_mus["latitude"])[0]), list(I_mus["museum"])[0]]
    else: 
        I_mus = stat.loc[(stat["name"]==list(top_stat["name"])[0])].head(1)
        path["1_museum"]=[(list(I_mus["longitude"])[0], list(I_mus["latitude"])[0]), list(I_mus["museum"])[0]]

    mus=pd.read_csv("mus_close_stat_filtered.csv")

    I_mus_stat = mus.loc[mus["museum"]==list(I_mus["museum"])[0]].head(1)
    path["1_museum_station"]=[(list(I_mus_stat["lon"])[0], list(I_mus_stat["lat"])[0]), list(I_mus_stat["name"])[0]]
    mus = mus.drop(mus[mus.museum == list(I_mus["museum"])[0]].index)
    stat = stat.drop(stat[stat.museum==list(I_mus["museum"])[0]].index)

    if count > 1:
        II_mus=stat.loc[(stat["name"]==list(I_mus_stat["name"])[0])].tail(1)
        path["2_museum"]= [(list(II_mus["longitude"])[0], list(II_mus["latitude"])[0]), list(II_mus["museum"])[0]]
        II_mus_stat = mus.loc[mus["museum"]==list(II_mus["museum"])[0]].head(1)
        path["2_museum_station"] = [(list(II_mus_stat["lon"])[0], list(II_mus_stat["lat"])[0]), list(II_mus_stat["name"])[0]]
        mus = mus.drop(mus[mus.museum == list(II_mus["museum"])[0]].index)
        stat = stat.drop(stat[stat.museum==list(II_mus["museum"])[0]].index)
    
    if count > 2:
        III_mus= stat.loc[(stat["name"]==list(II_mus_stat["name"])[0])].tail(1)
        path["3_museum"]= [(list(III_mus["longitude"])[0], list(III_mus["latitude"])[0]), list(III_mus["museum"])[0]]
        III_mus_stat = mus.loc[mus["museum"]==list(III_mus["museum"])[0]].head(1)
        path["3_museum_station"] = [(list(III_mus_stat["lon"])[0], list(III_mus_stat["lat"])[0]), list(III_mus_stat["name"])[0]]
        mus = mus.drop(mus[mus.museum == list(III_mus["museum"])[0]].index)
        stat = stat.drop(stat[stat.museum==list(III_mus["museum"])[0]].index)

    if count > 3:
        IV_mus= stat.loc[(stat["name"]==list(III_mus_stat["name"])[0])].tail(1)
        path["4_museum"]= [(list(IV_mus["longitude"])[0], list(IV_mus["latitude"])[0]), list(IV_mus["museum"])[0]]
        IV_mus_stat = mus.loc[mus["museum"]==list(IV_mus["museum"])[0]].head(1)
        path["4_museum_station"] = [(list(IV_mus_stat["lon"])[0], list(IV_mus_stat["lat"])[0]),list(IV_mus_stat["name"])[0]]
        mus = mus.drop(mus[mus.museum == list(IV_mus["museum"])[0]].index)
        stat = stat.drop(stat[stat.museum==list(IV_mus["museum"])[0]].index)
    
    if count > 4:
        V_mus= stat.loc[(stat["name"]==list(IV_mus_stat["name"])[0])].tail(1)
        path["5_museum"]= [(list(V_mus["longitude"])[0], list(V_mus["latitude"])[0]), list(V_mus["museum"])[0]]
        V_mus_stat = mus.loc[mus["museum"]==list(V_mus["museum"])[0]].head(1)
        path["5_museum_station"] = [(list(V_mus_stat["lon"])[0], list(V_mus_stat["lat"])[0]),list(V_mus_stat["name"])[0]]
        mus = mus.drop(mus[mus.museum == list(V_mus["museum"])[0]].index)
        stat = stat.drop(stat[stat.museum==list(V_mus["museum"])[0]].index)

    if count > 5:
        VI_mus= stat.loc[(stat["name"]==list(V_mus_stat["name"])[0])].tail(1)
        path["6_museum"]= [(list(VI_mus["longitude"])[0], list(VI_mus["latitude"])[0]), list(VI_mus["museum"])[0]]
        VI_mus_stat = mus.loc[mus["museum"]==list(VI_mus["museum"])[0]].head(1)
        path["6_museum_station"] = [(list(VI_mus_stat["lon"])[0], list(VI_mus_stat["lat"])[0]),list(VI_mus_stat["name"])[0]]

    return path

#user= random_pos_wash()
#path= user_path(user[0], user[1],3)

#print(json.dumps(path,indent=2))



