from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import time
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

try:
    start_time = time.time()
    client = MongoClient("mongodb+srv://s26827:Edgar12478@cluster0.eyfssrh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    db = client["tetris_db"]
    collection = db["scores"]
    logging.debug(f"MongoDB connection established in {time.time() - start_time} seconds.")
except Exception as e:
    logging.error(f"Error connecting to MongoDB: {e}")
    raise

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_score', methods=['POST'])
def save_score():
    data = request.json
    name = data.get('name')
    score = data.get('score')
    if name and score is not None:
        collection.insert_one({'name': name, 'score': score})
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error'}), 400

@app.route('/get_top_scores')
def get_top_scores():
    scores = list(collection.find().sort('score', -1).limit(10))
    return jsonify(scores)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=False)  
