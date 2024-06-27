# This script takes in data provided from the server and creates a graph showing
# the occupancy of grainger library from the past 6 hours as well as a predictive forcast 
# of the occupancy for the next 6 hours in the future.

import matplotlib
import requests
import pandas as pd
#import jsonify
node_id = 1
url = "http://192.168.71.126:5050"

response = requests.get(url+ "/data?node_id="+ str(node_id))

print(response.json())