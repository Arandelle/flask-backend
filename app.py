from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # ✅ Allow cross-origin requests (Next.js -> Flask)

# --- Sample data (pretend this came from a database) ---
transactions = [
    {"id": 1, "type": "income", "category": "Salary", "amount": 5000, "date": "2025-10-08"},
    {"id": 2, "type": "expense", "category": "Groceries", "amount": 800, "date": "2025-10-07"},
    {"id": 3, "type": "expense", "category": "Utilities", "amount": 1200, "date": "2025-10-05"},
]

@app.route('/api/transactions')
def get_transactions():
    return jsonify(transactions)

if __name__ == '__main__':
    app.run(debug=True)
