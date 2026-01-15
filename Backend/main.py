from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import os
import re
import PyPDF2
import unicodedata
import requests
from dotenv import load_dotenv

load_dotenv()

# Configuração do Flask
caminho_diretorio = os.path.abspath(os.path.dirname(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(caminho_diretorio, "..", "Templates"),
    static_folder=os.path.join(caminho_diretorio, "..", "Static")
)

UPLOAD_PASTA = os.path.join(caminho_diretorio, "..", "Upload")
EXTENSOES_PERMITIDAS = {"txt", "pdf"}
app.config["UPLOAD_PASTA"] = UPLOAD_PASTA
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5MB

if not os.path.exists(UPLOAD_PASTA):
    os.makedirs(UPLOAD_PASTA)

# Constantes
STOPWORDS = {
    "a", "à", "ao", "aos", "as", "até", "com", "da", "das", "de", "do", "dos",
    "e", "em", "na", "nas", "no", "nos",
    "o", "os", "para", "por", "que", "se", "sem", "um", "uma", "umas", "uns"
}

MAX_CHARS_PREPROCESS = 512

# Hugging Face API
HF_SENTIMENT_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2"
HF_SUMMARY_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
HF_TOKEN = os.environ.get("HF_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

# Funções auxiliares
def entrada_arquivo(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in EXTENSOES_PERMITIDAS


def preprocessar_texto(texto):
    texto = texto.lower()
    texto = re.sub(r"http\S+|www\S+|https\S+", "", texto)
    texto = re.sub(r"[^a-zA-Z0-9áàãâéêíóôõúç\s]", "", texto)
    texto = ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )
    tokens = texto.split()
    tokens = [t for t in tokens if t not in STOPWORDS]
    return " ".join(tokens)


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

# IA – Classificação
def classificar_sentimento(texto):
    try:
        payload = {"inputs": texto[:MAX_CHARS_PREPROCESS]}
        response = requests.post(
            HF_SENTIMENT_URL,
            headers=HEADERS,
            json=payload,
            timeout=10
        )
        data = response.json()

        if isinstance(data, list) and data:
            label = data[0]["label"].lower()
            score = float(data[0]["score"])
            if label == "positive" and score >= 0.85:
                return "Email Produtivo"

        return "Email Improdutivo"
    except Exception as e:
        print("Erro classificação IA:", e)
        return "Email Improdutivo"

# IA – Extração de Assunto
def extrair_assunto(texto):
    try:
        payload = {
            "inputs": texto[:MAX_CHARS_PREPROCESS],
            "parameters": {
                "max_length": 20,
                "min_length": 5
            }
        }
        response = requests.post(
            HF_SUMMARY_URL,
            headers=HEADERS,
            json=payload,
            timeout=10
        )
        data = response.json()

        if isinstance(data, list) and "summary_text" in data[0]:
            assunto = data[0]["summary_text"]
            return assunto.rstrip(".")
    except Exception as e:
        print("Erro extração assunto:", e)

    return "sua solicitação"

# Resposta controlada pelo backend
def gerar_resposta(categoria, assunto):
    if categoria == "Email Produtivo":
        return (
            f"Olá,\n\n"
            f"Recebemos sua solicitação referente a {assunto}. "
            f"Nossa equipe já está analisando e retornaremos em breve.\n\n"
            f"Atenciosamente,\nEquipe"
        )
    else:
        return (
            f"Olá,\n\n"
            f"Agradecemos sua mensagem. No momento, não é necessária nenhuma ação adicional.\n\n"
            f"Atenciosamente,\nEquipe"
        )

# Classificação híbrida
def classificar_email(texto):
    texto_lower = texto.lower()

    regras_improdutivas = [
        "promoção", "oferta", "newsletter", "marketing", "desconto",
        "liquidação", "sorteio", "brinde", "publicidade"
    ]

    palavras_produtivas = [
        "solicito", "aprovação", "erro", "problema", "prazo",
        "documento", "anexo", "formulário", "relatório"
    ]

    if any(p in texto_lower for p in regras_improdutivas):
        categoria = "Email Improdutivo"
    elif any(p in texto_lower for p in palavras_produtivas):
        categoria = "Email Produtivo"
    else:
        categoria = classificar_sentimento(texto)

    assunto = extrair_assunto(texto) if categoria == "Email Produtivo" else ""
    resposta = gerar_resposta(categoria, assunto)

    return {
        "category": categoria,
        "reply": resposta
    }

# Rotas
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analisar_email():
    try:
        email_text = request.form.get("emailText", "").strip()
        email_file = request.files.get("emailFile")

        if email_text and email_file:
            return jsonify({"error": "Envie apenas texto ou arquivo, não ambos."}), 400

        conteudo = ""
        if email_file and entrada_arquivo(email_file.filename):
            filename = secure_filename(email_file.filename)
            caminho = os.path.join(app.config["UPLOAD_PASTA"], filename)
            email_file.save(caminho)
            conteudo += ler_arquivo(caminho)

        if email_text:
            conteudo += " " + email_text

        if not conteudo.strip():
            return jsonify({"error": "Nenhum conteúdo encontrado."}), 400

        texto_limpo = preprocessar_texto(conteudo)
        resultado = classificar_email(texto_limpo)

        return jsonify(resultado)

    except Exception as e:
        print("ERRO INTERNO:", e)
        return jsonify({"error": "Erro interno do servidor"}), 500


@app.errorhandler(RequestEntityTooLarge)
def arquivo_grande(error):
    return jsonify({"error": "Arquivo muito grande. Limite máximo de 5MB."}), 413


# Rodar
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
