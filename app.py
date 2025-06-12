
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import openai
import os
from langdetect import detect
import json
from pathlib import Path
from vault_reader import query_vault

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")

# Carica prompt principale da file system_prompt.txt (mantiene il tono "professorone")
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
    return render_template("index.html")

@app.route('/query', methods=['POST'])
def query():
    user_input = request.json.get('input', '')

    # Check difensivo: evitare domande tipo "sei chatgpt?"
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

    # Risposta con contesto integrato (ma sempre usando il prompt "professorone")
    user_prompt = user_input
    if TESLA_PROFILE:
        projects = TESLA_PROFILE.get("organization", {}).get("notable_projects", [])
        persona_info = f"\n\nContext: Current active projects include: " + ", ".join(projects)
        user_prompt += persona_info

    # Integrazione Vault
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
