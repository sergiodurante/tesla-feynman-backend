
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import openai
import os

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")

with open("system_prompt.txt") as f:
    system_prompt = f.read()

@app.route('/')
def interface():
    return render_template("index.html")

@app.route('/query', methods=['POST'])
def query():
    user_input = request.json.get('input', '')
    if any(term in user_input.lower() for term in ["chatgpt", "openai", "gpt-4", "are you real"]):
        return jsonify({"response": "Mi spiace, non posso rispondere a questa domanda. 🛡️"})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        temperature=0.7
    )
    return jsonify({"response": response.choices[0].message.content.strip()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
