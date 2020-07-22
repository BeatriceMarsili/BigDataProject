#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import geopy.distance 


# In[168]:


def random_pos_wash():
    "Returns a random point on Washington territory"
    lon=randint(-77087171, -76971923, 1)
    lat= randint(38857369 ,38938736, 1)
    return lon[0]/1000000, lat[0]/1000000


def user_path(lon, lat):
    "Given longitude and latitude returns a list of stations and museums"
    stat=pd.read_csv("stat_close_mus_filt.csv")
    stat = stat.drop('Unnamed: 0', 1)
    stat_point = list(zip(stat.lon, stat.lat))
    current= np.inf 
    for el in stat_point:
        dist = geopy.distance.distance((lon, lat), el).miles
        if current > dist:
            current=dist 
            top_stat = stat.loc[(stat['lat'] == el[1]) & (stat["lon"]==el[0])]
    print  ("First Station to go:", list(top_stat["lon"])[0], list(top_stat["lat"])[0], list(top_stat["name"])[0])
    if list(top_stat["region_id"])[0]==42.0:
        I_mus = stat.loc[(stat["name"]==list(top_stat["name"])[0])].tail(1)
        print("First museum to go:", list(I_mus["longitude"])[0], list(I_mus["latitude"])[0], list(I_mus["museum"])[0])
    else: 
        I_mus = stat.loc[(stat["name"]==list(top_stat["name"])[0])].head(1)
        print("First museum to go:", list(I_mus["longitude"])[0], list(I_mus["latitude"])[0], list(I_mus["museum"])[0])
    
    mus=pd.read_csv("mus_close_stat_filt.csv")
    
    I_mus_stat = mus.loc[mus["museum"]==list(I_mus["museum"])[0]].head(1)
    print("Closest station to museum:", list(I_mus_stat["lon"])[0], list(I_mus_stat["lat"])[0],
          list(I_mus_stat["name"])[0])
    mus = mus.drop(mus[mus.museum == list(I_mus["museum"])[0]].index)
    stat = stat.drop(stat[stat.museum==list(I_mus["museum"])[0]].index)




    II_mus=stat.loc[(stat["name"]==list(I_mus_stat["name"])[0])].tail(1)
    print("Second museum to go:", list(II_mus["longitude"])[0], list(II_mus["latitude"])[0], list(II_mus["museum"])[0])
    II_mus_stat = mus.loc[mus["museum"]==list(II_mus["museum"])[0]].head(1)
    print("Closest station to museum:", list(II_mus_stat["lon"])[0], list(II_mus_stat["lat"])[0],
          list(II_mus_stat["name"])[0])
    mus = mus.drop(mus[mus.museum == list(II_mus["museum"])[0]].index)
    stat = stat.drop(stat[stat.museum==list(II_mus["museum"])[0]].index)

    
    III_mus= stat.loc[(stat["name"]==list(II_mus_stat["name"])[0])].tail(1)
    print("Third museum to go:", list(III_mus["longitude"])[0], list(III_mus["latitude"])[0], list(III_mus["museum"])[0])
    III_mus_stat = mus.loc[mus["museum"]==list(III_mus["museum"])[0]].head(1)
    print("Closest station to museum:", list(III_mus_stat["lon"])[0], list(III_mus_stat["lat"])[0],
          list(III_mus_stat["name"])[0])
    mus = mus.drop(mus[mus.museum == list(III_mus["museum"])[0]].index)
    stat = stat.drop(stat[stat.museum==list(III_mus["museum"])[0]].index)
    
    IV_mus= stat.loc[(stat["name"]==list(III_mus_stat["name"])[0])].tail(1)
    print("Fourth museum to go:", list(IV_mus["longitude"])[0], list(IV_mus["latitude"])[0], list(IV_mus["museum"])[0])
    IV_mus_stat = mus.loc[mus["museum"]==list(IV_mus["museum"])[0]].head(1)
    print("Closest station to museum:", list(IV_mus_stat["lon"])[0], list(IV_mus_stat["lat"])[0],
          list(IV_mus_stat["name"])[0])
    mus = mus.drop(mus[mus.museum == list(IV_mus["museum"])[0]].index)
    stat = stat.drop(stat[stat.museum==list(IV_mus["museum"])[0]].index)
    
    V_mus= stat.loc[(stat["name"]==list(IV_mus_stat["name"])[0])].tail(1)
    print("Fifth museum to go:", list(V_mus["longitude"])[0], list(V_mus["latitude"])[0], list(V_mus["museum"])[0])
    V_mus_stat = mus.loc[mus["museum"]==list(V_mus["museum"])[0]].head(1)
    print("Closest station to museum:", list(V_mus_stat["lon"])[0], list(V_mus_stat["lat"])[0],
          list(V_mus_stat["name"])[0])
    mus = mus.drop(mus[mus.museum == list(V_mus["museum"])[0]].index)
    stat = stat.drop(stat[stat.museum==list(V_mus["museum"])[0]].index)

    
    VI_mus= stat.loc[(stat["name"]==list(V_mus_stat["name"])[0])].tail(1)
    print("Sixth museum to go:", list(VI_mus["longitude"])[0], list(VI_mus["latitude"])[0], list(VI_mus["museum"])[0])
    VI_mus_stat = mus.loc[mus["museum"]==list(VI_mus["museum"])[0]].head(1)
    print("Closest station to museum:", list(VI_mus_stat["lon"])[0], list(VI_mus_stat["lat"])[0],
          list(VI_mus_stat["name"])[0])

    
    return ((list(top_stat["lon"])[0], list(top_stat["lat"])[0]), 
            (list(I_mus_stat["lon"])[0], list(I_mus_stat["lat"])[0]), 
            (list(I_mus["longitude"])[0], list(I_mus["latitude"])[0]),
            (list(I_mus_stat["lon"])[0], list(I_mus_stat["lat"])[0]), 
            (list(II_mus_stat["lon"])[0], list(II_mus_stat["lat"])[0]),
            (list(II_mus["longitude"])[0], list(II_mus["latitude"])[0]),
            (list(II_mus_stat["lon"])[0], list(II_mus_stat["lat"])[0]),
            (list(III_mus_stat["lon"])[0], list(III_mus_stat["lat"])[0]),
            (list(III_mus["longitude"])[0], list(III_mus["latitude"])[0]),
            (list(III_mus_stat["lon"])[0], list(III_mus_stat["lat"])[0]),
            (list(IV_mus_stat["lon"])[0], list(IV_mus_stat["lat"])[0]),
            (list(IV_mus["longitude"])[0], list(IV_mus["latitude"])[0]),
            (list(IV_mus_stat["lon"])[0], list(IV_mus_stat["lat"])[0]),
            (list(V_mus_stat["lon"])[0], list(V_mus_stat["lat"])[0]),
            (list(V_mus["longitude"])[0], list(V_mus["latitude"])[0]),
            (list(V_mus_stat["lon"])[0], list(V_mus_stat["lat"])[0]),
            (list(VI_mus_stat["lon"])[0], list(VI_mus_stat["lat"])[0]),
            (list(VI_mus["longitude"])[0], list(VI_mus["latitude"])[0]),
            (list(VI_mus_stat["lon"])[0], list(VI_mus_stat["lat"])[0]))


# In[185]:


user= random_pos_wash()
user_path(user[0], user[1])

