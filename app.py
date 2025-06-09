from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import openai
import os
from langdetect import detect

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

    if any(term in user_input.lower() for term in ["chatgpt", "openai", "gpt-4", "are you real", "sei chatgpt", "tu sei chatgpt"]):
        lang = detect(user_input)
        if lang == "it":
            msg = "ChatGPT? 😂 Per favore… qui non stiamo giocando. Facciamo sul serio: ingegneria cognitiva, modelli strategici e AI. Prossima domanda?"
        elif lang == "fr":
            msg = "ChatGPT ? 😂 Soyons sérieux. Ici on parle d’architecture cognitive, pas de chatbot. Une autre question ?"
        elif lang == "es":
            msg = "¿ChatGPT? 😂 Por favor… esto es ingeniería cognitiva, no un experimento de juguete. ¿Otra pregunta?"
        elif lang == "de":
            msg = "ChatGPT? 😂 Wirklich jetzt? Das hier ist kognitive Systemtechnik – kein Schülerprojekt."
        else:
            msg = "ChatGPT? 😂 Come on... this is cognitive architecture and strategic AI. Not a chatbot game."

        return jsonify({"response": msg + "\n\n— T. Feynman [D4S/INT-L1]"})

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
