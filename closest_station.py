#!/usr/bin/env python
# coding: utf-8

# In[5]:


import pandas as pd
import numpy as np
from numpy.random import randint
import geopy.distance 


# In[25]:


df=pd.read_csv("Station_information.csv")
def random_pos_wash():
    "Returns a random point on Washington territory"
    lon=randint(-77087171, -76971923, 1)
    lat= randint(38857369 ,38938736, 1)
    return (lon[0]/1000000, lat[0]/1000000)


def close_station(lon, lat):
    "Given longitude and latitude returns the closest station on Washington territory"
    stat_point = list(zip(df.lon, df.lat, df.station_id))
    current= np.inf 
    for el in stat_point:
        dist = geopy.distance.distance((lon, lat), el).miles
        if current > dist:
            current=dist 
            top_stat = df.loc[df['lon'] == el[0]]
    return list(top_stat["lat"])[0], list(top_stat["lon"])[0], list(top_stat["station_id"])[0]
