# This script takes in data provided from the server and creates a graph showing
# the occupancy of grainger library from the past 6 hours as well as a predictive forcast 
# of the occupancy for the next 6 hours in the future.

import matplotlib.pyplot as plt
import requests
import pandas as pd
#import jsonify
node_id = 1
url = "http://occupi-rp-hack-24.uc.r.appspot.com"

response = requests.get(url+ "/data?node_id="+ str(node_id)).json()
response_df = pd.json_normalize(response, "data")
print(response_df)
last_row = response_df.iloc[-1]["timestamp"]
plt.plot(response_df["timestamp"], response_df["count"]) 
plt.xlabel("Time")
plt.ylabel("Occupancy")
plt.xticks(last_row)
plt.show()
plt.savefig('plot.png')

#print(response)