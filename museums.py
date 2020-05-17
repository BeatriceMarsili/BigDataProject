#custom file to save some configurations
from utilities import *
from privates import *

import json
import pandas as pd
import urllib.request
import hashlib

#Washington DC museums lists, actually containing just the DC opendata references
#To enlarge the dataset just add more urls and check that they follow the same format.
#If not, write some code to modifiy those data accodingly:
#OBJECTID - (NAME) - ALT_NAME - LABEL - (MAR_MATCHADDRESS) - MAR_XCOORD - MAR_YCOORD - (MAR_LONGITUDE) - (MAR_LATITUDE) - MARID

museums_url = [
	"https://opendata.arcgis.com/datasets/2e65fc16edc3481989d2cc17e6f8c533_54.geojson"
]
museums_full_results = []

for url in museums_url:
	get_response = urllib.request.urlopen(url)
	museums_full_results.append(json.loads(get_response.read()))

museums_pruned = [
	museums_full_results[0]["features"]
]

debug = False

#Place here the code to format the different urls and insert them inside the "museums_pruned" array
#Care only about the NAME - MAR_MATCHADDRESS - MAR_LONGITUDE - MAR_LATITUDE attributes, the others wont be used

museums_clean = {"museums":[]}

for mset in museums_pruned:
	for element in mset:
		if debug:
			print(json.dumps(element,indent=2))
		
		basic = {
			"name":element["properties"]["NAME"],
			"address":element["properties"]["MAR_MATCHADDRESS"],
			"longitude":element["properties"]["MAR_LONGITUDE"],
			"latitude":element["properties"]["MAR_LATITUDE"]
		}

		museums_clean["museums"].append(basic)

if debug:
	print(json.dumps(museums_clean,indent=2))

#At this point the "formatted_clean" dictionary contains a JSON like structure with all the relevant data 
#needed for the google Places API. Since the API could be very expensive the data are cached inside the "cache" folder.
#The name are univocally translated into hashes to standardize the operation.
encrypter = hashlib.md5()

for element in museum_clean:
	


encrypter.update(().encode('utf-8'))
unique_name = encrypter.hexdigest()


#creates dictionary from JSON station_information
base = "https://maps.googleapis.com/maps/api/place/details/json?"

complete = base + "key=" + google_key + "&place_id="
print(complete)


