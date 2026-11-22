from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
import json
import os

app = Flask(__name__)

client = MongoClient(os.environ.get('MONGO_URI'))
db = client['todo_db']
collection = db['todos']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api')
def api():
    with open('data.json') as f:
        data = json.load(f)
    return jsonify(data)

@app.route('/submittodoitem', methods=['POST'])
def submit_todo_item():
    data = request.get_json(silent=True) or request.form
    item = {
        'itemName': data.get('itemName'),
        'itemDescription': data.get('itemDescription')
    }
    collection.insert_one(item)
    return jsonify({'message': 'Item stored successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True)
