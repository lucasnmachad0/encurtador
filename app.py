from flask import Flask, request, redirect
import json
import os
import random
import string

app = Flask(__name__)
ARQUIVO_URLS = "urls.json"

if not os.path.exists(ARQUIVO_URLS):
    with open(ARQUIVO_URLS, "w", encoding="utf-8") as f:
        json.dump({}, f)


def carregar_urls():
    with open(ARQUIVO_URLS, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_urls(dados):
    with open(ARQUIVO_URLS, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2)


def gerar_codigo(tamanho=6):
    caracteres = string.ascii_letters + string.digits
    return "".join(random.choice(caracteres) for _ in range(tamanho))


PAGINA = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Encurtador de URL</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 0 15px rgba(0,0,0,0.1);
            text-align: center;
            width: 400px;
        }
        input[type="text"] {
            width: 90%;
            padding: 10px;
            margin-bottom: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        button {
            padding: 10px 20px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        button:hover { background-color: #45a049; }
        .resultado { margin-top: 20px; word-break: break-all; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Encurtador de URL</h1>
        <form method="POST" action="/">
            <input type="text" name="url" placeholder="Cole sua URL longa aqui" required>
            <button type="submit">Encurtar</button>
        </form>
        {% if link_curto %}
        <div class="resultado">
            <p>Seu link encurtado:</p>
            <a href="{{ link_curto }}" target="_blank">{{ link_curto }}</a>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def index():
    link_curto = None

    if request.method == "POST":
        url_longa = request.form["url"]
        urls = carregar_urls()

        codigo = gerar_codigo()
        while codigo in urls:
            codigo = gerar_codigo()

        urls[codigo] = url_longa
        salvar_urls(urls)

        link_curto = request.host_url + codigo

    from flask import render_template_string
    return render_template_string(PAGINA, link_curto=link_curto)


@app.route("/<codigo>")
def redirecionar(codigo):
    urls = carregar_urls()
    url_original = urls.get(codigo)

    if url_original:
        return redirect(url_original)
    return "Link não encontrado :(", 404


if __name__ == "__main__":
    app.run(debug=True)