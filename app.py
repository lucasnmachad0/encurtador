from flask import Flask, request, redirect, render_template
import json
import os
import random
import string

app = Flask(__name__)

ARQUIVO_URLS = "urls.json"

# Cria o arquivo de URLs se ele ainda não existir
if not os.path.exists(ARQUIVO_URLS):
    with open(ARQUIVO_URLS, "w", encoding="utf-8") as f:
        json.dump({}, f)


def carregar_urls():
    """Lê o arquivo JSON e devolve um dicionário {codigo: url_original}."""
    with open(ARQUIVO_URLS, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_urls(dados):
    """Salva o dicionário atualizado de volta no arquivo JSON."""
    with open(ARQUIVO_URLS, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)


def gerar_codigo(tamanho=6):
    """Gera um código aleatório de letras e números."""
    caracteres = string.ascii_letters + string.digits
    return "".join(random.choice(caracteres) for _ in range(tamanho))


@app.route("/", methods=["GET", "POST"])
def index():
    link_curto = None

    if request.method == "POST":
        url_longa = request.form["url"]
        urls = carregar_urls()

        # Gera um código e garante que não existe outro igual
        codigo = gerar_codigo()
        while codigo in urls:
            codigo = gerar_codigo()

        urls[codigo] = url_longa
        salvar_urls(urls)

        link_curto = request.host_url + codigo

    return render_template("index.html", link_curto=link_curto)


@app.route("/<codigo>")
def redirecionar(codigo):
    urls = carregar_urls()
    url_original = urls.get(codigo)

    if url_original:
        return redirect(url_original)

    return render_template("erro.html"), 404


if __name__ == "__main__":
    app.run(debug=True)