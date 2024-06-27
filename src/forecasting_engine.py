import requests 
import numpy as np
import pandas as pd
import os
from dotenv import load_dotenv
from flask import jsonify

node_id = 1
load_dotenv("../.env")
url = os.getenv('API_URL')

def get_data(start=None, end=None):
    if not start and not end:
        response = requests.get(url + "/data")
    elif not start:
        response = requests.get(url + f"/data?node_id=1&start={start}")
    elif not end:
        response = requests.get(url + f"/data?node_id=1&end={end}")
    else:
        response = requests.get(url + f"/data?node_id=1&start={start}&end={end}")

    json_file = response.json()
    pd_df = pd.DataFrame(json_file)

    return pd_df

def write_forecast(df, node_id = 1):
    json_str = df.to_json(orient='records')
    return requests.post(url + f"/forecast?node_id=1", jsonify(json_str))