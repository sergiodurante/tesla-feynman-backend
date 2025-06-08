from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)

@app.route('/query', methods=['POST'])
def query():
    user_input = request.json.get('input', '')
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are Tesla Feynman, an advanced cognitive architecture co-developed with human input. Respond clearly and insightfully."},
            {"role": "user", "content": user_input}
        ],
        temperature=0.7
    )
    return jsonify({"response": response.choices[0].message.content.strip()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
