import requests
import json
from flask import Flask, render_template, request, jsonify

from cs50 import SQL
#conectar ao data base

db = SQL("sqlite:///if.db")

app = Flask(__name__)



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
    response = requests.post(1, headers=headers, data=json.dumps(data))
    return response


@app.route("/", methods=["GET", "POST"])
def home():

    return render_template("index.html")
        

@app.route("/contatos", methods=["GET", "POST"])
def contatos():
    return render_template("contatos.html")

@app.route("/calendario", methods=["GET", "POST"])
def calendario():
    if request.method == "POST":
        dia = request.form["dia"]
        texto=request.form["texto"]
        mes =request.form["mes"]
        title =request.form["titulo"]
        db.execute("INSERT INTO Calendario (day, month, title, texto) VALUES (?, ?, ?, ?)",dia, mes, title, texto)

    calendario = db.execute("SELECT * from Calendario")


    return render_template("calendario.html")

if __name__ == "__main__":
    app.run(debug=True)
