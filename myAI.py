import os
from dotenv import load_dotenv
import google.generativeai as genai
from flask import Flask, request, jsonify

load_dotenv()
app = Flask(__name__)

# Configure the Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

@app.route('/api/ask_ai', methods=['POST'])
def ask_ai():
    data = request.get_json()
    user_prompt = data.get("prompt")

    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(user_prompt)

    return jsonify({"reply": response.text})

# 👇 This part starts the Flask app
if __name__ == '__main__':
    app.run(debug=True)
