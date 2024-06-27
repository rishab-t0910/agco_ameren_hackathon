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
        response = requests.get(url + "/data").json()
    elif not start:
        response = requests.get(url + f"/data?node_id=1&start={start}").json()
    elif not end:
        response = requests.get(url + f"/data?node_id=1&end={end}").json()
    else:
        response = requests.get(url + f"/data?node_id=1&start={start}&end={end}").json()

    pd_df = pd.json_normalize(response, "data")
    return pd_df

def write_forecast(df, node_id = 1):
    json_str = df.to_json(orient='records')
    response = requests.post(url + "/forecast?node_id=" + str(node_id), json=json_str)