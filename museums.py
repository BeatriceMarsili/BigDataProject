from urllib.request import Request, urlopen
#custom file to save some configurations
from utilities import *

import json
import pandas as pd

#creates dictionary from JSON station_information
base = "https://maps.googleapis.com/maps/api/place/details/json?"
place_id = "ChIJyWEHuEmuEmsRm9hTkapTCrk"

complete = base + "key=" + google_key + "&place_id=" + place_id
print(complete)

