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

STOPWORDS = {
    "a", "à", "ao", "aos", "as", "até", "com", "da", "das", "de", "do", "dos",
    "e", "em", "na", "nas", "no", "nos",
    "o", "os", "para", "por", "que", "se", "sem", "um", "uma", "umas", "uns"
}

MAX_CHARS_PREPROCESS = 512  # Limite para análise NLP

#  HUGGING FACE API
HF_API_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2"
HF_TOKEN = os.environ.get("HF_TOKEN") 
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

def analisar_sentimento_hf(texto):
    try:
        texto = texto[:MAX_CHARS_PREPROCESS]  # Limitar caracteres
        response = requests.post(HF_API_URL, headers=HEADERS, json={"inputs": texto}, timeout=10)
        data = response.json()
        if isinstance(data, list) and len(data) > 0 and "label" in data[0]:
            label = data[0]["label"].lower()
            score = float(data[0]["score"])
            categoria = "Email Produtivo" if label == "positive" and score >= 0.85 else "Email Improdutivo"
            return categoria
        return "Email Improdutivo"
    except Exception as e:
        print("Erro Hugging Face API:", e)
        return "Email Improdutivo"

#  Funções 
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

def gerar_resposta(categoria):
    if categoria == "Email Produtivo":
        return (
            "Olá, recebemos sua solicitação e nossa equipe está analisando cuidadosamente. "
            "Entraremos em contato assim que houver uma atualização relevante. "
            "Agradecemos pelo seu contato e pela confiança em nossos serviços."
        )
    else:
        return (
            "Olá, agradecemos por sua mensagem. No momento, nenhuma ação adicional é necessária. "
            "Caso haja qualquer informação relevante no futuro, entraremos em contato. "
            "Obrigado pelo seu contato."
        )

# Classificação híbrida
def classificar_email_hibrido(texto):
    texto_lower = texto.lower()
    regras_improdutivas = [
        "marketing","newsletter","promoção","oferta","publicidade",
        "spam","propaganda","anúncio","desconto","venda",
        "compre agora","clique aqui","inscreva-se","assinatura",
        "garanta já","última chance","exclusivo","imperdível",
        "brinde","cupom","sorteio","concursos","liquidação"
    ]
    palavras_acao = [
        "solicito","verificar","analisar","erro","problema",
        "reunião","prazo","documento","anexo",
        "confirmação","retorno","atualização","encaminho", "poderia"
    ]

    if any(p in texto_lower for p in regras_improdutivas):
        categoria = "Email Improdutivo"
    elif any(p in texto_lower for p in palavras_acao):
        categoria = "Email Produtivo"
    else:
        categoria = analisar_sentimento_hf(texto)

    return {"category": categoria, "reply": gerar_resposta(categoria)}

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
            return jsonify({"error": "Por favor, envie apenas texto ou arquivo, não ambos."}), 400

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
        resultado = classificar_email_hibrido(texto_limpo)
        return jsonify(resultado)

    except Exception as e:
        print("ERRO INTERNO:", e)
        return jsonify({"error": f"Erro interno do servidor: {str(e)}"}), 500

@app.errorhandler(RequestEntityTooLarge)
def arquivo_grande(error):
    return jsonify({"error": "Arquivo muito grande. O tamanho máximo permitido é 5MB."}), 413

# Execução da aplicação
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
