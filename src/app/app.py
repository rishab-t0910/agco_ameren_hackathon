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
    return None

@app.route('/data', methods=['GET'])
def get_data():
    return None

@app.route('/count', methods=['GET'])
def get_count():
    return None

@app.route('/forecast', methods=['GET'])
def get_forecast():
    return None