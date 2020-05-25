#!/usr/bin/env python
# coding: utf-8

# In[178]:


import json
import pandas as pd
import urllib.request
from datetime import datetime, timezone
import pytz


# In[179]:


url_station = "https://gbfs.capitalbikeshare.com/gbfs/es/station_information.json"


# In[180]:


response_station = urllib.request.urlopen(url_station)
data_station = json.loads(response_station.read())
dic_station = {}
i=0
for el in data_station["data"]["stations"]:
    dic_station[i]=el
    i+=1
#creates dictionary from JSON station_information


# In[181]:


df_station = pd.DataFrame.from_dict(dic_station, orient = 'index')
#transforms dictionary to df 


# In[182]:


#converts to actual date time the last_updated field in the original JSON
timestamp_station = data_station["last_updated"]
time_zone = pytz.timezone("US/Eastern")
last_updated_station = datetime.fromtimestamp(timestamp_station).astimezone(time_zone).strftime('%Y-%m-%d %H:%M:%S')


# In[183]:


station = pd.concat([df_station["station_id"],
                     df_station["name"],
                     df_station["rental_methods"],
                     df_station["lat"],
                     df_station["lon"], 
                     df_station["capacity"], 
                     df_station["region_id"],
                     df_station["station_type"]], axis=1)
#keeps relevant information


# In[184]:


url_status = "https://gbfs.capitalbikeshare.com/gbfs/es/station_status.json"


# In[185]:


response_status = urllib.request.urlopen(url_status)
data_status = json.loads(response_status.read())
dic_status = {}
i=0
for el in data_status["data"]["stations"]:
    dic_status[i]=el
    i+=1
#creates dictionary from JSON station_status


# In[186]:


df_status = pd.DataFrame.from_dict(dic_status, orient = 'index')  #transforms dictionary to df 


# In[187]:


#converts to actual date time the last_updated field in the original JSON
timestamp_status = data_status["last_updated"]
last_updated_status = datetime.fromtimestamp(timestamp_status).astimezone(time_zone).strftime('%Y-%m-%d %H:%M:%S')


# In[188]:


#adds column last_reported_date with human readable date
for el in df_status["last_reported"]:
    df_status["last_reported_date"] = datetime.fromtimestamp(el).astimezone(time_zone).strftime("%Y-%m-%d %H:%M:%S")


# In[189]:


status = pd.concat([df_status["station_id"],
                    df_status["num_bikes_available"],
                    df_status["num_docks_available"], 
                    df_status["num_ebikes_available"], 
                    df_status["num_bikes_disabled"],
                    df_status["num_docks_disabled"], 
                    df_status["last_reported_date"],
                    df_status["is_renting"], 
                    df_status["is_returning"]], axis=1)
#keeps relevant info only


# In[190]:


last_updated_station


# In[191]:


last_updated_status


# In[192]:


#inner joins the two datasets in one on station_id column
station_status = status.join(station.set_index(['station_id'], 
                                               verify_integrity=True ), 
                             on=[ 'station_id' ], 
                             how='right' )


# In[193]:


station_status = station_status.rename(columns={'name': 'Station_Name'})


# In[194]:


df_distances = pd.read_csv("Mus_Stat_closest.csv")


# In[195]:


df_distances['MUSEUM'].value_counts()  #number of stations fount for each museum


# In[198]:


#joins the file with museums and their closest stations with informations about stations and their status 
actual_status = df_distances.merge(station_status, on=('Station_Name'), how='inner')  


# In[205]:


#normalizing values: bikes and docks available keeps into account the disabled ones, and then removes irrelevant cols
actual_status["num_bikes_available"] = actual_status["num_bikes_available"] - actual_status["num_bikes_disabled"]
actual_status["num_docks_available"] = actual_status["num_docks_available"] - actual_status["num_docks_disabled"]
actual_status = actual_status.drop(['num_bikes_disabled', 'num_docks_disabled'], axis=1)


# In[207]:


#this is just a reduced version of the above to have a quick look of our data
quick_look = pd.concat([actual_status["MUSEUM"],
                             actual_status["Station_Name"],
                             actual_status["approx_distance_miles"],
                             actual_status["num_bikes_available"],
                             actual_status["num_docks_available"],
                             actual_status["num_ebikes_available"],
                             actual_status["capacity"]], axis=1)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




