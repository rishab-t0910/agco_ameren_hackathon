from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os
from database_handler import DatabaseHandler

app = Flask(__name__)
CORS(app)

db = DatabaseHandler()

@app.route('/count', methods=['GET'])
def get_count():
    return None