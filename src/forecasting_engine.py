import requests 
import numpy as np
import pandas as pd
import os
from dotenv import load_dotenv

node_id = 1
load_dotenv("../.env")
url = os.getenv('API_URL')

def get_data(start=None, end=None):
    if not start and not end:
        response = requests.get(url)
    elif not start:
        response = requests.get()