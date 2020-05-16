from urllib.request import Request, urlopen
import json
import pandas as pd

#custom file to save some configurations
from utilities import *

#creates dictionary from JSON station_information
base = "https://maps.googleapis.com/maps/api/place/details/json?"
place_id = "ChIJyWEHuEmuEmsRm9hTkapTCrk"

complete = base + "key=" + google_key + "&place_id=" + place_id
print(complete)

