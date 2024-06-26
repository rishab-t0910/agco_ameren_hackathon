from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os
from database_handler import DatabaseHandler

app = Flask(__name__)
CORS(app)

db = DatabaseHandler()

@app.route('/add', methods=['POST'])
def add_entry():
    """
    Add a document (single observation) to the dataset. This request should have
    a JSON payload as follows:
    node_id
    sensor data
    count
    """
    return None

@app.route('/data', methods=['GET'])
def get_data():
    """
    Get all streaming data from raspberry pi. This route should have parameters
    like follows: "/data?node_id=<x>&start=<y>&end=<z>" where
    node_id: node id
    start: start timestamp
    end: end timestamp
    """
    return None

@app.route('/count', methods=['GET'])
def get_count():
    """
    Get current (real-time) counts of data. This route should have parameters
    like follows: "/count?node_id=<x>" where
    node_id: node id
    """
    return None

@app.route('/forecast', methods=['GET'])
def get_forecast():
    """
    Get forecast for a node id. Returns observations for the last 6 hours and
    forecasts for the next 6 hours. This route should have parameters like 
    follows: "/forecast?node_id=<x>&time=<y>" where
    node_id: node id
    time: timestamp to get forecast (prev 6 and next 6 hours)
    """
    return None