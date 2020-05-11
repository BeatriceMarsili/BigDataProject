import json
import pandas as pd
import urllib.request
from datetime import datetime, timezone
import pytz

#creates dictionary from JSON station_information
url_station = "https://gbfs.capitalbikeshare.com/gbfs/es/station_information.json"
response_station = urllib.request.urlopen(url_station)
data_station = json.loads(response_station.read())
dic_station = {}
i=0
for el in data_station["data"]["stations"]:
    dic_station[i]=el
    i+=1
#transforms dictionary to df 
df_station = pd.DataFrame.from_dict(dic_station, orient = 'index')
#converts to actual date time the last_updated field in the original JSON
timestamp_station = data_station["last_updated"]
time_zone = pytz.timezone("US/Eastern")
last_updated_station = datetime.fromtimestamp(timestamp_station).astimezone(time_zone).strftime('%Y-%m-%d %H:%M:%S')

#keeps relevant information
station = pd.concat([df_station["station_id"],
                     df_station["name"],
                     df_station["rental_methods"],
                     df_station["lat"],
                     df_station["lon"], 
                     df_station["capacity"], 
                     df_station["region_id"],
                     df_station["station_type"]], axis=1)

#creates dictionary from JSON station_status
url_status = "https://gbfs.capitalbikeshare.com/gbfs/es/station_status.json"
response_status = urllib.request.urlopen(url_status)
data_status = json.loads(response_status.read())
dic_status = {}
i=0
for el in data_status["data"]["stations"]:
    dic_status[i]=el
    i+=1
df_status = pd.DataFrame.from_dict(dic_status, orient = 'index')  #transforms dictionary to df 

timestamp_status = data_status["last_updated"]
last_updated_status = datetime.fromtimestamp(timestamp_status).astimezone(time_zone).strftime('%Y-%m-%d %H:%M:%S')

#adds column last_reported_date with human readable date
for el in df_status["last_reported"]:
    df_status["last_reported_date"] = datetime.fromtimestamp(el).astimezone(time_zone).strftime("%Y-%m-%d %H:%M:%S")

#keeps relevant info only
status = pd.concat([df_status["station_id"],
                    df_status["num_bikes_available"],
                    df_status["num_docks_available"], 
                    df_status["num_ebikes_available"], 
                    df_status["num_bikes_disabled"],
                    df_status["num_docks_disabled"], 
                    df_status["last_reported_date"],
                    df_status["is_renting"], 
                    df_status["is_returning"]], axis=1)

station_status = status.join(station.set_index(['station_id'], verify_integrity=True ), on=[ 'station_id' ], how='left' )

