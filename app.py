from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import hashlib

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Connect to local MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['wedding']
collection = db['rsvp']

@app.route('/api/rsvp', methods=['POST'])
def rsvp():
    data = request.get_json()
    name = data.get('name')
    tel = data.get('tel')
    rsvp = data.get('rsvp')
    unique_string = f"{name}{tel}{rsvp}"
    unique_id = hashlib.sha256(unique_string.encode()).hexdigest()
    collection.insert_one({'_id': unique_id, 'name': name, 'tel': tel, 'rsvp': rsvp})
    return jsonify({'message': 'RSVP received', 'data': data}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5004)