from flask import Flask, request, redirect, render_template
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
    # utf-8-sig ignora o caractere invisível (BOM) que o Windows
    # às vezes adiciona no início do arquivo
    with open(ARQUIVO_URLS, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def salvar_urls(dados):
    with open(ARQUIVO_URLS, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)


def gerar_codigo(tamanho=6):
    caracteres = string.ascii_letters + string.digits
    return "".join(random.choice(caracteres) for _ in range(tamanho))


@app.route("/", methods=["GET", "POST"])
def index():
    link_curto = None

    if request.method == "POST":
        url_longa = request.form["url"]
        urls = carregar_urls()

        codigo = gerar_codigo()
        while codigo in urls:
            codigo = gerar_codigo()

        urls[codigo] = {
            "url": url_longa,
            "cliques": 0
        }
        salvar_urls(urls)

        link_curto = request.host_url + codigo

    return render_template("index.html", link_curto=link_curto)


@app.route("/<codigo>")
def redirecionar(codigo):
    urls = carregar_urls()
    entrada = urls.get(codigo)

    if entrada:
        entrada["cliques"] += 1
        salvar_urls(urls)
        return redirect(entrada["url"])

    return render_template("erro.html"), 404


@app.route("/estatisticas")
def estatisticas():
    urls = carregar_urls()
    return render_template("estatisticas.html", urls=urls)


if __name__ == "__main__":
    app.run(debug=True)
