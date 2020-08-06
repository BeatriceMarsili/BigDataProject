#!/usr/bin/env python
# coding: utf-8

# In[16]:


import pandas as pd
import numpy as np
import geopy.distance 
from numpy.random import randint


# In[17]:


def random_pos_wash():
    "Returns a random point on Washington territory"
    lon=randint(-77087171, -76971923, 1)
    lat= randint(38857369 ,38938736, 1)
    return lon[0]/1000000, lat[0]/1000000


# In[57]:


def user_path(lon, lat):
    "Given longitude and latitude returns a list of 6 museums and related stations"

    stat=pd.read_csv("stat_close_mus_filt.csv")
    stat = stat.drop(stat[stat.avlb_bikes ==False].index)
    stat = stat.drop(stat[stat.avlb_docks ==False].index)  
    stat = stat.drop('Unnamed: 0', 1)
    stat_point = list(zip(stat.lon, stat.lat))
    current= np.inf
    path= {}
    for el in stat_point:
        dist = geopy.distance.distance((lon, lat), el).miles
        if current > dist:
            current=dist 
            top_stat = stat.loc[(stat['lat'] == el[1]) & (stat["lon"]==el[0])]
    path["First_station"]=[(list(top_stat["lon"])[0], list(top_stat["lat"])[0]), list(top_stat["name"])[0]]
    if list(top_stat["region_id"])[0]==42.0:
        I_mus = stat.loc[(stat["name"]==list(top_stat["name"])[0])].tail(1)
        path["First_museum"]=[(list(I_mus["longitude"])[0], list(I_mus["latitude"])[0]), list(I_mus["museum"])[0]]
    else: 
        I_mus = stat.loc[(stat["name"]==list(top_stat["name"])[0])].head(1)
        path["First_museum"]=[(list(I_mus["longitude"])[0], list(I_mus["latitude"])[0]), list(I_mus["museum"])[0]]

    mus=pd.read_csv("mus_close_stat_filt.csv")
    mus = mus.drop(mus[mus.avlb_bikes ==False].index)
    mus = mus.drop(mus[mus.avlb_docks ==False].index)

    I_mus_stat = mus.loc[mus["museum"]==list(I_mus["museum"])[0]].head(1)
    path["First_museum_station"]=[(list(I_mus_stat["lon"])[0], list(I_mus_stat["lat"])[0]), list(I_mus_stat["name"])[0]]
    mus = mus.drop(mus[mus.museum == list(I_mus["museum"])[0]].index)
    stat = stat.drop(stat[stat.museum==list(I_mus["museum"])[0]].index)

    II_mus=stat.loc[(stat["name"]==list(I_mus_stat["name"])[0])].tail(1)
    path["Second_museum"]= [(list(II_mus["longitude"])[0], list(II_mus["latitude"])[0]), list(II_mus["museum"])[0]]
    II_mus_stat = mus.loc[mus["museum"]==list(II_mus["museum"])[0]].head(1)
    path["Second_museum_station"] = [(list(II_mus_stat["lon"])[0], list(II_mus_stat["lat"])[0]), list(II_mus_stat["name"])[0]]
    mus = mus.drop(mus[mus.museum == list(II_mus["museum"])[0]].index)
    stat = stat.drop(stat[stat.museum==list(II_mus["museum"])[0]].index)

    III_mus= stat.loc[(stat["name"]==list(II_mus_stat["name"])[0])].tail(1)
    path["Third_museum"]= [(list(III_mus["longitude"])[0], list(III_mus["latitude"])[0]), list(III_mus["museum"])[0]]
    III_mus_stat = mus.loc[mus["museum"]==list(III_mus["museum"])[0]].head(1)
    path["Third_museum_station"] = [(list(III_mus_stat["lon"])[0], list(III_mus_stat["lat"])[0]), list(III_mus_stat["name"])[0]]

    mus = mus.drop(mus[mus.museum == list(III_mus["museum"])[0]].index)
    stat = stat.drop(stat[stat.museum==list(III_mus["museum"])[0]].index)

    IV_mus= stat.loc[(stat["name"]==list(III_mus_stat["name"])[0])].tail(1)
    path["Fourth_museum"]= [(list(IV_mus["longitude"])[0], list(IV_mus["latitude"])[0]), list(IV_mus["museum"])[0]]

    IV_mus_stat = mus.loc[mus["museum"]==list(IV_mus["museum"])[0]].head(1)
    path["Fourth_museum_station"] = [(list(IV_mus_stat["lon"])[0], list(IV_mus_stat["lat"])[0]),
          list(IV_mus_stat["name"])[0]]

    mus = mus.drop(mus[mus.museum == list(IV_mus["museum"])[0]].index)
    stat = stat.drop(stat[stat.museum==list(IV_mus["museum"])[0]].index)

    V_mus= stat.loc[(stat["name"]==list(IV_mus_stat["name"])[0])].tail(1)
    path["Fifth_museum"]= [(list(V_mus["longitude"])[0], list(V_mus["latitude"])[0]), list(V_mus["museum"])[0]]

    V_mus_stat = mus.loc[mus["museum"]==list(V_mus["museum"])[0]].head(1)
    path["Fifth_museum_station"] = [(list(V_mus_stat["lon"])[0], list(V_mus_stat["lat"])[0]),
          list(V_mus_stat["name"])[0]]

    mus = mus.drop(mus[mus.museum == list(V_mus["museum"])[0]].index)
    stat = stat.drop(stat[stat.museum==list(V_mus["museum"])[0]].index)


    VI_mus= stat.loc[(stat["name"]==list(V_mus_stat["name"])[0])].tail(1)
    path["Sixth_museum"]= [(list(VI_mus["longitude"])[0], list(VI_mus["latitude"])[0]), list(VI_mus["museum"])[0]]

    VI_mus_stat = mus.loc[mus["museum"]==list(VI_mus["museum"])[0]].head(1)
    path["Sixth_museum_station"] = [(list(VI_mus_stat["lon"])[0], list(VI_mus_stat["lat"])[0]),
          list(VI_mus_stat["name"])[0]]

    
    return path


# In[66]:


user= random_pos_wash()
path= user_path(user[0], user[1])


# In[73]:





# In[ ]:




