from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/count', methods=['GET'])
def get_count():
    return None