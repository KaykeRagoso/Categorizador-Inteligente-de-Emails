from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

import os
import re
import PyPDF2
from transformers import pipeline


# Configurações
caminho_diretorio = os.path.abspath(os.path.dirname(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(caminho_diretorio, "..", "Templates"),
    static_folder=os.path.join(caminho_diretorio, "..", "Static")
)

UPLOAD_PASTA = os.path.join(caminho_diretorio, "..", "Upload")
EXTENSOES_PERMITIDAS = {"txt", "pdf"}

app.config["UPLOAD_PASTA"] = UPLOAD_PASTA
app.config["MAX_CONTENT_LENGTH"] = 7 * 1024 * 1024  # 7MB

if not os.path.exists(UPLOAD_PASTA):
    os.makedirs(UPLOAD_PASTA)

# NLP LOCAL
sentiment_analyzer = None

def get_sentiment_analyzer():
    global sentiment_analyzer
    if sentiment_analyzer is None:
        sentiment_analyzer = pipeline(
            "sentiment-analysis",
            model="distilbert/distilbert-base-uncased-finetuned-sst-2-english"
        )
    return sentiment_analyzer

def entrada_arquivo(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in EXTENSOES_PERMITIDAS


def limpar_texto(texto):
    texto = texto.lower()
    texto = re.sub(r"[^a-zA-Z0-9áàãâéêíóôõúç\s]", "", texto)
    texto = re.sub(r"\s+", " ", texto)
    return texto.strip()


def ler_arquivo(caminho_arquivo):
    ext = caminho_arquivo.rsplit(".", 1)[1].lower()

    if ext == "txt":
        with open(caminho_arquivo, "r", encoding="utf-8") as file:
            return file.read()

    elif ext == "pdf":
        texto = ""
        with open(caminho_arquivo, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                texto += page.extract_text() or ""
        return texto

    return ""


def classificar_email_hibrido(texto):
    texto = texto.lower()

    regras_improdutivas = [
        "Marketing","newsletter", "promoção", "oferta", "publicidade",
        "spam", "propaganda", "anúncio", "desconto", "venda",
        "compre agora", "clique aqui", "inscreva-se", "assinatura",
        "garanta já", "última chance", "exclusivo", "imperdível",
        "brinde", "cupom", "sorteio", "concursos", "liquidação"
    ]

    palavras_acao = [
        "solicito", "verificar", "analisar", "erro", "problema",
        "reunião", "prazo", "documento", "anexo",
        "confirmação", "retorno", "atualização", "encaminho"
    ]

    # Camada 1 – improdutivo explícito
    if any(p in texto for p in regras_improdutivas):
        return {
            "category": "Email Improdutivo",
            "reply": "Olá! Obrigado pela mensagem. Nenhuma ação é necessária no momento."
        }

    # Camada 2 – produtivo por intenção
    if any(p in texto for p in palavras_acao):
        return {
            "category": "Email Produtivo",
            "reply": "Olá! Recebemos sua solicitação e nossa equipe irá analisar o quanto antes."
        }

    # Camada 3 – NLP (desempate)
    analyzer = get_sentiment_analyzer()
    resultado = analyzer(texto[:512])[0]  # Limitar a 512 caracteres para melhor desempenho

    if resultado["label"].lower() == "positive" and resultado["score"] >= 0.85:
        return {
            "category": "Email Produtivo",
            "reply": "Olá! Seu email foi recebido e será tratado pela equipe responsável."
        }

    return {
        "category": "Email Improdutivo",
        "reply": "Olá! Obrigado pelo contato. Não é necessária nenhuma ação adicional."
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analisar_email():
    email_text = request.form.get("emailText", "")
    email_file = request.files.get("emailFile")

    conteudo = ""

    if email_file and entrada_arquivo(email_file.filename):
        filename = secure_filename(email_file.filename)
        caminho = os.path.join(app.config["UPLOAD_PASTA"], filename)
        email_file.save(caminho)
        conteudo += ler_arquivo(caminho)

    if email_text.strip():
        conteudo += " " + email_text

    if not conteudo.strip():
        return jsonify({"error": "Nenhum conteúdo encontrado."}), 400

    texto_limpo = limpar_texto(conteudo)
    resultado = classificar_email_hibrido(texto_limpo)

    return jsonify( resultado)


@app.errorhandler(RequestEntityTooLarge)
def arquivo_grande(error):
    return jsonify({
        "error": "Arquivo muito grande. O tamanho máximo permitido é 7MB."
    }), 413


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
