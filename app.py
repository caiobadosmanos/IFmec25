import requests
import json
from flask import Flask, render_template, request, jsonify

from cs50 import SQL
#conectar ao data base

db = SQL("sqlite:///if.db")

app = Flask(__name__)

# Chave de API diretamente no código
API_KEY = 'AIzaSyAIOAHZsjsWQ8rP7NTI4QsWBtI7XuEauiY'
API_URL = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}'

# Variável global para armazenar o input do usuário
user_input = ""
resposta = None  # Inicializa a variável global resposta


def call_api(user_input):
    """Função para enviar requisição para a API."""
    data = {
        "contents": [{
            "parts": [{"text": user_input}]
        }]
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(API_URL, headers=headers, data=json.dumps(data))
    return response


@app.route("/", methods=["GET", "POST"])
def home():

    return render_template("index.html")
        

@app.route("/contatos", methods=["GET", "POST"])
def contatos():
    return render_template("contatos.html")

@app.route("/calendario", methods=["GET", "POST"])
def calendario():

    return render_template("calendario.html")

if __name__ == "__main__":
    app.run(debug=True)
