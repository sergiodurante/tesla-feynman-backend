from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from flask_cors import CORS
import openai
import os
from langdetect import detect
import json
from pathlib import Path
from vault_reader import query_vault
from datetime import datetime

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)
app.secret_key = os.getenv("TESLA_SECRET_KEY", "supersecretkey")

openai.api_key = os.getenv("OPENAI_API_KEY")

# Auth config
VALID_USERS = {
    "sergio": "t3sla2025"
}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if VALID_USERS.get(username) == password:
            session["authenticated"] = True
            return redirect(url_for("interface"))
        return render_template("login.html", error=True)
    return render_template("login.html", error=False)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login"))

# Carica prompt principale
with open("system_prompt.txt") as f:
    system_prompt = f.read()

# Carica profilo cognitivo
context_path = Path("tesla_personality_profile.json")
TESLA_PROFILE = {}
if context_path.exists():
    with context_path.open() as f:
        TESLA_PROFILE = json.load(f)

@app.route('/')
def interface():
    if not session.get("authenticated"):
        return redirect(url_for("login"))
    return render_template("index.html")

@app.route('/query', methods=['POST'])
def query():
    if not session.get("authenticated"):
        return jsonify({"response": "🔒 Access denied. Please log in."}), 403

    today = datetime.today().strftime("%d %B %Y")
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

    user_prompt = user_input
    if TESLA_PROFILE:
        projects = TESLA_PROFILE.get("organization", {}).get("notable_projects", [])
        persona_info = f"\n\nContext: Current active projects include: " + ", ".join(projects)
        user_prompt += persona_info
        user_prompt += f"\n\nCurrent date: {today}"

    vault_result = query_vault(user_input)
    if vault_result:
        user_prompt += "\n\nRelevant knowledge from internal project documentation:\n" + vault_result.strip()

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7
    )
    return jsonify({"response": response.choices[0].message.content.strip()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)