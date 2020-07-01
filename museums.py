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
def elaborate():
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

	errors = 0

	for element in museums_clean["museums"]:
		data = {}
		if not connect_online_API:
			#use the cached local files, which are saved with an unique MD5 hash
			encrypter = hashlib.md5()
			encrypter.update((element['name']).encode('utf-8'))
			filename = "./cache/" + encrypter.hexdigest() + ".json"

			with open(filename) as json_file:
				data = json.load(json_file) 

			if debug:
				print("data loaded from cached source")

		else:
			#query google places to gather all the required informations
			base_url_search = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?"
			complete_search = base_url_search + "key=" + google_key + "&inputtype=textquery&input=" + (element["name"].lower().replace(" ","%20")).replace("\r\n","") + "%20washingtondc"
			
			##test until the API is not operative
			search_response = urllib.request.urlopen(complete_search)
			search_result = json.loads(search_response.read())

			#save the place id, fundamental for the detail research
			if search_result['candidates'] != []:
				element["place_id"] = search_result["candidates"][0]["place_id"]
				if debug:
					print(element)
			else:
				element["place_id"] = 0
			
			if element["place_id"] != 0:

				base_url_details = "https://maps.googleapis.com/maps/api/place/details/json?"
				complete_details = base_url_details + "key=" + google_key + "&place_id=" + element["place_id"]
				
				##test until the API is not operative
				details_response = urllib.request.urlopen(complete_details)
				data = json.loads(details_response.read())

				#Now the "data" variable contains an instance of the downloaded data from the google query
				#If we need to cache those data we store it (obviously only if they come from the internet)

				if cache_local:
					encrypter = hashlib.md5()
					encrypter.update((element['name']).encode('utf-8'))
					filename = "./cache/" + encrypter.hexdigest() + ".json"

					with open(filename, 'w+') as json_file:
					    json.dump(data, json_file)

				if debug:
					cache_string = ""
					if cache_local:
						cache_string = "not"
					print("data loaded from google API source and " + cache_string + " cached locally")

		#Now we proceed with the extraction of the relevant data from the "data" variabile - NOTE: data is actually kinda a bad name, will refactor it
		#permanently closed?
		if data["status"] == "OK":
			main_info = data["result"]
			#save the phone number as a string (might be useless, but whatever)
			
			if "international_phone_number" in main_info:
				element["phone_number"] = main_info["international_phone_number"]
			if "permanently_closed" in main_info:
				element["permanently_closed"] = main_info["permanently_closed"]

			#opening_hours. Actually not formatted, will agree on a standard
			if "opening_hours" in main_info:
				element["opening_hours"] = main_info["opening_hours"]
			if "rating" in main_info:
				element["rating"] = main_info["rating"]
			if "website" in main_info:
				element["website"] = main_info["website"]
		else:
			errors=errors+1

	if debug:
		if errors == 0:
			print("Data fetching complete without errors")
		else:
			print("Data fetching complete. " + str(errors) + " errors found. Data might be incomplete")

	with open("museums.json", 'w+') as json_file:
	    json.dump(museums_clean, json_file)

	return museums_clean

#standalone execution
#elaborate()