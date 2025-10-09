from flask import Flask, jsonify, request
from flask_cors import CORS # to handle CORS issues
from pymongo import MongoClient # for mongoDB connection
from dotenv import load_dotenv # to load environment variables from .env file
import os # for environment variables
from bson import ObjectId # to handle ObjectId from MongoDB


load_dotenv() # load environment variables from .env file

app = Flask(__name__)
CORS(app)  # ✅ Allow cross-origin requests (Next.js -> Flask)

# Get mongo uri from environment variable
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["coinwise"] # database name
collections = db["transactions"] # collection name

# GET retrieve all transactions
@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    transactions = list(collections.find({}, {"_id" : 0})) # exclude _id field
    return jsonify(transactions)

# GET by ID - retrieve a single transaction
@app.route('/api/transactions/<transaction_id>', methods=['GET'])
def get_transaction(transaction_id):
    transaction = collections.find_one({"_id" : ObjectId(transaction_id)})
    if transaction:
        transaction["_id"] = str(transaction["_id"]) # convert objectId to string
        return jsonify(transaction)
    return jsonify({"error" : "Transaction not found"}), 404

# POST - create a new transaction
@app.route('/api/transactions', methods=['POST'])

def add_transaction():
    data = request.get_json() # get JSON data from request body
    if not data:
        return jsonify({"error" : "No data provided"}), 400
    result = collections.insert_one(data) # insert data into collection
    return jsonify({"message" : "Transaction added", "id" : str(result.inserted_id)}), 201

# PUT - update an existing transaction
@app.route('/api/transactions/<transaction_id>', methods=["PUT"])
def update_transaction(transaction_id):
    data = request.get_json()
    result = collections.update_one(
        {"_id" : ObjectId(transaction_id)}, # filter by id
        {"$set" : data} # update with new data
        )
    if result.matched_count == 0:
        return jsonify({"error": "Transaction not found"}), 404
    return jsonify({"message": "Transaction updated"}), 200

# DELETE - delete a transaction
@app.route("/api/transactions/<transaction_id>", methods=["DELETE"])
def delete_transaction(transaction_id):
    result = collections.delete_one({"_id" : ObjectId(transaction_id)})
    if result.deleted_count == 0:
        return jsonify({"error" : "Transaction not found"}), 404
    return jsonify({"message" : "Transaction deleted"}), 200

@app.route('/')
def index():
    return "Flask backend is running!"
if __name__ == '__main__':
    app.run(debug=True)
