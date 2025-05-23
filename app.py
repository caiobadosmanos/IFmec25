import requests
import json
from flask import Flask, render_template, request, jsonify,redirect
from datetime import date

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
        if "delete" in request.form:
            title =request.form["titulo"]
            

            db.execute("DELETE FROM Calendario WHERE title = ?", title)
            redirect("/calendario")

        if request.is_json:
                    data = request.get_json()
                    dia = data["dia"]
                    mes = data["mes"]
                    titulo = data["titulo"]
                    texto = data.get("texto", "")
                    db.execute("INSERT INTO Calendario (day, month, title, texto) VALUES (?, ?, ?, ?)", dia, mes, titulo, texto)
                    return jsonify({"status": "ok"})

                    


        if "dia" in request.form:
            dia = request.form["dia"]
            texto=request.form["texto"]
            mes =request.form["mes"]
            title =request.form["titulo"]
            print(dia, mes, title, texto)
            db.execute("INSERT INTO Calendario (day, month, title, texto) VALUES (?, ?, ?, ?)",dia, mes, title, texto)
            redirect("/calendario")

    calendario = db.execute("SELECT * from Calendario")

    #converte para jonson
    json_formatado = [
        {
            "title": evento["title"],
            "start": f"2025-{evento['month']:02d}-{evento['day']:02d}",
            "extendedProps": {
                "texto": evento["texto"]
            }
        }
        for evento in calendario
    ]


    print(calendario)


    return render_template("calendario.html",eventos=json_formatado)

@app.route("/adicionar", methods=["GET", "POST"])
def adicionar():
    if request.method == "POST":
         if "dia" in request.form:
            dia = request.form["dia"]
            texto=request.form["texto"]
            mes =request.form["mes"]
            title =request.form["titulo"]
            print(dia, mes, title, texto)
            db.execute("INSERT INTO Calendario (day, month, title, texto) VALUES (?, ?, ?, ?)",dia, mes, title, texto)
            redirect("/calendario")


    return render_template("adicionar.html")
        
@app.route("/deletar", methods=["GET", "POST"])
def deletar():
    if request.method == "POST":
        if "delete" in request.form:
            title =request.form["titulo"]
            

            db.execute("DELETE FROM Calendario WHERE title = ?", title)
            redirect("/calendario")


    return render_template("deletar.html")
        
if __name__ == "__main__":
    app.run(debug=True)
