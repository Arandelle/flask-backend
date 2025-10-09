from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # ✅ Allow cross-origin requests (Next.js -> Flask)

# --- Sample data (pretend this came from a database) ---
transactions = [
    {"id": 1, "type": "income", "category": "Salary", "amount": 5000, "date": "2025-10-08"},
    {"id": 2, "type": "expense", "category": "Groceries", "amount": 800, "date": "2025-10-07"},
    {"id": 3, "type": "expense", "category": "Utilities", "amount": 1200, "date": "2025-10-05"},
]

# GET retrieve all transactions
@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    return jsonify(transactions)

# GET by ID - retrieve a single transaction

@app.route('/api/transactions/<int:transaction_id>', methods=['GET'])
def get_transaction(transaction_id):
    transactions_found = next((t for t in transactions if t["id"] == transaction_id), None)
    if transactions_found:
        return jsonify(transactions_found), 200
    return jsonify({"error": "Transaction not found"}), 404

# POST - create a new transaction
@app.route('/api/transactions', methods=['POST'])

def add_transaction():
    data = request.get_json() # get JSON data from request body
    if not data:
        return jsonify({"error" : "Invalid input"}), 400
    
    new_id = max(t["id"] for t in transactions) + 1 if transactions else 1
    new_transcation = {
        "id" : new_id,
        "type" : data.get("type"),
        "category" : data.get("category"),
        "amount" : data.get("amount"),
        "date" : data.get("date")
    }
    transactions.append(new_transcation)
    return jsonify(new_transcation), 201

# PUT - update an existing transaction
@app.route('/api/transactions/<int:transaction_id>', methods=["PUT"])
def update_transaction(transaction_id):
    data = request.get_json()
    for t in transactions:
        if t["id"] == transaction_id:
            t.update({
                "type" : data.get("type", t["type"]),
                "category" : data.get("category", t["category"]),
                "amount" : data.get("amount", t["amount"]),
                "date" : data.get("date", t["date"])
            })
            return jsonify(t), 200
    
    return jsonify({"error": "Transaction not found"}), 404

# DELETE - delete a transaction
@app.route("/api/transactions/<int:transaction_id>", methods=["DELETE"])
def delete_transaction(transaction_id):
    global transactions
    transactions = [t for t in transactions if t["id"] != transaction_id]
    return jsonify({"message" : "Transaction deleted"}), 200

@app.route('/')
def index():
    return "Flask backend is running!"
if __name__ == '__main__':
    app.run(debug=True)
