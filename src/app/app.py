from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from database_handler import DatabaseHandler
import datetime

app = Flask(__name__)
CORS(app)

db = DatabaseHandler()

@app.route('/add', methods=['POST'])
def add_entry():
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
        return "Missing data", 400

    db.add_data(node_id, timestamp, noise, count)
    return "Success", 200

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
        return "Missing data", 400
    
    try:
        start_timestamp = datetime.datetime.strptime('%Y-%m-%dT%H:%M:%S') if start else None
        end_timestamp = datetime.datetime.strptime('%Y-%m-%dT%H:%M:%S') if end else None
    except ValueError:
        return jsonify({'error': 'Invalid datetime format. Use YYYY-MM-DDTHH:MM:SS'}), 400


    if start_timestamp and end_timestamp and start_timestamp >= end_timestamp:
        return jsonify({'error': 'Start time must be before end time'}), 400
    
    try:
        data = db.get_data(node_id, start_timestamp, end_timestamp)
        return jsonify ({'data' : data}), 200
    except Exception as e:
        return jsonify({'error' : str(e)}), 400

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)