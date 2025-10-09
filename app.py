from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
import os

# Load environment variable locally
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# CORS configuration
CORS(app, resources={
    r"/api/*": {"origins": [
        "http://localhost:3000",
        "http://localhost:3001",
        "https://coinwise-opal.vercel.app"
    ]}
})

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("MONGO_URI environment variable not set")

try:
    client = MongoClient(MONGO_URI, tls=True)  # proper SSL
    db = client["coinwise"]
    collections = db["transactions"]
except Exception as e:
    print("Failed to connect to MongoDB:", e)
    raise e

# Routes
@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    try:
        transactions = list(collections.find({}, {"_id": 0}))
        return jsonify(transactions)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/transactions/<transaction_id>', methods=['GET'])
def get_transaction(transaction_id):
    try:
        transaction = collections.find_one({"_id": ObjectId(transaction_id)})
        if transaction:
            transaction["_id"] = str(transaction["_id"])
            return jsonify(transaction)
        return jsonify({"error": "Transaction not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/transactions', methods=['POST'])
def add_transaction():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    try:
        result = collections.insert_one(data)
        return jsonify({"message": "Transaction added", "id": str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/transactions/<transaction_id>', methods=['PUT'])
def update_transaction(transaction_id):
    data = request.get_json()
    try:
        result = collections.update_one({"_id": ObjectId(transaction_id)}, {"$set": data})
        if result.matched_count == 0:
            return jsonify({"error": "Transaction not found"}), 404
        return jsonify({"message": "Transaction updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/transactions/<transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    try:
        result = collections.delete_one({"_id": ObjectId(transaction_id)})
        if result.deleted_count == 0:
            return jsonify({"error": "Transaction not found"}), 404
        return jsonify({"message": "Transaction deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    return "Flask backend is running!"

if __name__ == '__main__':
    app.run(debug=True)
