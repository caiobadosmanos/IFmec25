import requests
import json
from flask import Flask, render_template, request, jsonify


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
    global user_input  # Declaração para usar a variável global
    global resposta  # Declaração para usar a variável global

    if request.method == "POST":
        # Obtém o tipo de requisição (normal ou botão "Gerar Novamente")
        action = request.form.get("action", "question")

        if action == "question":
            # Solicita ao usuário o conteúdo
            user_input = request.form.get("question")

            if not user_input:
                return jsonify({"resposta": "Por favor, forneça os ingredientes."})

            # Adiciona formatação específica ao input
            user_input += (
                "obs: ao invés de usar sua formatação normal use <bold>para negrito</bold>, "
                "<ul><li>para listas</li><li>não ordenadas</li></ul> <p>para parágrafos</p> "
                "e <ol><li>para listas</li><li>que são ordenadas</li></ol>, e não cite essas ordens no seu output;"
            )

        elif action == "gerar_novamente":
            # Ajusta o input para gerar uma receita inusitada
            user_input += " obs: tente algo que vc nao tentaria"

        # Chama a API
        response = call_api(user_input)

        if response.status_code == 200:
            response_data = response.json()
            resposta = response_data['candidates'][0]['content']['parts'][0]['text']
            return jsonify({"resposta": resposta})
        else:
            return jsonify({"resposta": f"Erro {response.status_code}: {response.text}"})

    return render_template("index.html", resposta=resposta)


@app.route("/contatos", methods=["GET", "POST"])
def contatos():
    return render_template("contatos.html")


if __name__ == "__main__":
    app.run(debug=True)
