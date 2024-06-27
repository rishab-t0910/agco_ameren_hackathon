from flask import Flask, jsonify, request, send_from_directory, send_file
from flask_cors import CORS
from dotenv import load_dotenv
from .database_handler import DatabaseHandler
from .graph_generation import generate_graph
import datetime
from io import BytesIO
import matplotlib.pyplot as plt
import requests
import pandas as pd

app = Flask(__name__, static_folder='../website')
CORS(app)

db = DatabaseHandler()

def parse_timestamp(timestamp):
    return datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S')

@app.route('/')
def index():
    return send_from_directory('../website', 'index.html')

@app.route('/graph', methods=['GET'])
def generate_graph():
    node_id = request.args.get('node_id')
    
    response = get_data.json()
    response_df = pd.json_normalize(response, "data")
    print(response_df)
    last_row = response_df.iloc[-1]["timestamp"]
    plt.figure(figsize=(18,6))
    plt.plot(response_df["timestamp"], response_df["count"]) 
    plt.xlabel("Time")
    plt.ylabel("Occupancy")
    plt.xticks(last_row)
    
    img_io = BytesIO()
    plt.savefig(img_io, format='png')
    img_io.seek(0)
    plt.close()

    return send_file(img_io, mimetype='image/png')

@app.route('/add', methods=['POST'])
def add_data():
    """
    Add a document (single observation) to the dataset. This request should have
    a JSON payload as follows:
    node_id: rpi uuid
    timestamp: rpi timestamp at read time
    noise: noise levels
    count: edge computed occupancy count
    """
    data = request.get_json()
    node_id = data.get('node_id')
    timestamp = data.get('timestamp')
    noise = data.get('noise')
    count = data.get('count')

    if node_id is None:
        return jsonify({'error': 'Missing data'}), 400

    db.add_data(node_id, timestamp, noise, count)
    return jsonify({'message': 'Success'}), 200

@app.route('/data', methods=['GET'])
def get_data():
    """
    Get all streaming data from raspberry pi. This route should have parameters
    like follows: "/data?node_id=<x>&start=<y>&end=<z>" where
    node_id: node id
    start: start timestamp
    end: end timestamp
    """
    node_id = request.args.get('node_id')
    start = request.args.get('start')
    end = request.args.get('end')

    if node_id is None:
        return jsonify({'error': 'Missing data'}), 400
    
    try:
        start_timestamp = parse_timestamp(start) if start else None
        end_timestamp = parse_timestamp(end) if end else None
    except ValueError:
        return jsonify({'error': 'Invalid datetime format. Use YYYY-MM-DDTHH:MM:SS'}), 400


    if start_timestamp and end_timestamp and start_timestamp >= end_timestamp:
        return jsonify({'error': 'Start time must be before end time'}), 400
    
    try:
        data = db.get_data(node_id, start_timestamp, end_timestamp)
        return jsonify ({'data' : data}), 200
    except Exception as e:
        return jsonify({'error' : str(e)}), 500

@app.route('/count', methods=['GET'])
def get_most_recent_count():
    """
    Get current (real-time) counts of data. This route should have parameters
    like follows: "/count?node_id=<x>" where
    node_id: node id
    """
    node_id = request.args.get('node_id')

    if node_id is None:
        return jsonify({'error': 'Missing data'}), 400
    
    try:
        # Query Firestore for the most recent document
        count = db.get_most_recent_count(node_id)
        if count is not None:
            return jsonify({'node_id': node_id, 'count': count}), 200
        else:
            return jsonify({'error': 'No data found for node_id'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route('/forecast', methods=['GET', 'POST'])
def forecast():
    """
    GET
    Get forecast for a node id. Returns observations for the last 6 hours and
    forecasts for the next 6 hours. This route should have parameters like 
    follows: "/forecast?node_id=<x>&time=<y>" where
    node_id: node id
    time: timestamp to get forecast (prev 6 and next 6 hours)

    POST
    Post a forecast to the database. Expects a JSON payload as follows:
    node_id: node id
    timestamp: future timestamp
    count: forecasted count
    """
    if request.method == 'GET':
        node_id = request.args.get('node_id')
        timestamp = request.args.get('time')

        if not node_id or not timestamp:
            return jsonify({'error': 'Missing node_id or timestamp parameter'}), 400

        try:
            time = parse_timestamp(timestamp)
        except ValueError:
            return jsonify({'error': 'Invalid datetime format. Use YYYY-MM-DDTHH:MM:SS'}), 400

        try:
            data = db.get_forecast(node_id, time)
            return jsonify({'data' : data}), 200
        except Exception as e:
            return jsonify({'error' : str(e)}), 500
    

    elif request.method == 'POST':
        data = request.get_json()
        try:
            # Rewrite the forecast collection with updated forecast data
            db.set_forecast(1, data)
            return jsonify({'message': 'Forecast data updated successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return None

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)