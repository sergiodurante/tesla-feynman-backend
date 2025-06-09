from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import openai

openai.api_key = "sk-test-TEMPORARY-KEY-1234567890"

app = Flask(__name__)
CORS(app)

html_content = """<!DOCTYPE html>
<html lang='en'>
<head>
  <meta charset='UTF-8'>
  <meta name='viewport' content='width=device-width, initial-scale=1.0'/>
  <title>Tesla Feynman | Strategic Cognitive Interface</title>
  <style>
    body {
      background-color: #0f0f0f;
      color: #e0e0e0;
      font-family: 'Courier New', Courier, monospace;
      margin: 0;
      padding: 2rem;
    }
    h1 {
      font-size: 1.6rem;
      color: #66ccff;
      border-bottom: 1px solid #444;
      padding-bottom: 0.5rem;
    }
    #interface {
      max-width: 800px;
      margin: 0 auto;
    }
    .label {
      margin-top: 2rem;
      font-weight: bold;
      color: #999;
    }
    textarea, .response {
      width: 100%;
      background-color: #1a1a1a;
      color: #f1f1f1;
      border: 1px solid #333;
      padding: 1rem;
      margin-top: 0.5rem;
      resize: vertical;
      font-size: 1rem;
    }
    .response {
      min-height: 150px;
      white-space: pre-wrap;
    }
    .signature {
      color: #aaa;
      font-size: 0.9rem;
      margin-top: 2rem;
      border-top: 1px solid #333;
      padding-top: 1rem;
    }
    button {
      margin-top: 1rem;
      padding: 0.7rem 1.5rem;
      background-color: #222;
      color: #66ccff;
      border: 1px solid #444;
      cursor: pointer;
    }
  </style>
</head>
<body>
  <div id='interface'>
    <h1>Tesla Feynman [D4S/INT-L1]<br>Strategic Cognitive Interface</h1>

    <div class='label'>Input:</div>
    <textarea id='userInput' placeholder='Enter your query, observation or scenario...'></textarea>
    <button onclick='sendQuery()'>Ask Tesla</button>

    <div class='label'>Response:</div>
    <div id='response' class='response'>Awaiting input...</div>
  </div>

  <script>
    async function sendQuery() {
      const input = document.getElementById('userInput').value;
      document.getElementById('response').innerText = 'Processing...';
      console.log("SendQuery triggered with input:", input); // DEBUG

      try {
        const res = await fetch('/query', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ input: input })
        });
        const data = await res.json();
        document.getElementById('response').innerText = data.response + '\n\nT. Feynman [D4S/INT-L1]\nCognitive Architecture – Durante Space Tech';
      } catch (err) {
        console.error("Fetch error:", err); // DEBUG
        document.getElementById('response').innerText = "⚠️ Error: " + err;
      }
    }
  </script>
</body>
</html>"""

@app.route('/')
def interface():
    return render_template_string(html_content)

@app.route('/query', methods=['POST'])
def query():
    user_input = request.json.get('input', '')
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are Tesla Feynman, an advanced cognitive architecture co-developed with human input. Respond clearly and insightfully."},
            {"role": "user", "content": user_input}
        ],
        temperature=0.7
    )
    return jsonify({"response": response.choices[0].message.content.strip()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
