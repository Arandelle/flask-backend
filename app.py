from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from bson import ObjectId

load_dotenv()

app = Flask(__name__)

# ✅ Configure CORS to allow your Next.js frontend
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:3000",
            "http://localhost:3001",
            "https://coinwise-opal.vercel.app/"  # Add your production URL here
        ],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Get mongo uri from environment variable
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["coinwise"]
collections = db["transactions"]

# GET retrieve all transactions
@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    transactions = list(collections.find({}, {"_id": 0}))
    return jsonify(transactions)

# GET by ID - retrieve a single transaction
@app.route('/api/transactions/<transaction_id>', methods=['GET'])
def get_transaction(transaction_id):
    transaction = collections.find_one({"_id": ObjectId(transaction_id)})
    if transaction:
        transaction["_id"] = str(transaction["_id"])
        return jsonify(transaction)
    return jsonify({"error": "Transaction not found"}), 404

# POST - create a new transaction
@app.route('/api/transactions', methods=['POST'])
def add_transaction():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    result = collections.insert_one(data)
    return jsonify({"message": "Transaction added", "id": str(result.inserted_id)}), 201

# PUT - update an existing transaction
@app.route('/api/transactions/<transaction_id>', methods=["PUT"])
def update_transaction(transaction_id):
    data = request.get_json()
    result = collections.update_one(
        {"_id": ObjectId(transaction_id)},
        {"$set": data}
    )
    if result.matched_count == 0:
        return jsonify({"error": "Transaction not found"}), 404
    return jsonify({"message": "Transaction updated"}), 200

# DELETE - delete a transaction
@app.route("/api/transactions/<transaction_id>", methods=["DELETE"])
def delete_transaction(transaction_id):
    result = collections.delete_one({"_id": ObjectId(transaction_id)})
    if result.deleted_count == 0:
        return jsonify({"error": "Transaction not found"}), 404
    return jsonify({"message": "Transaction deleted"}), 200

@app.route('/')
def index():
    return "Flask backend is running!"

if __name__ == '__main__':
    app.run(debug=True)