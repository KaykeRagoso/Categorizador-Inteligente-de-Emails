from flask import Flask, request,jsonify, render_template
from werkzeug.utils import secure_filename

import os
import re
import PyPDF2

caminho_diretorio = os.path.abspath(os.path.dirname(__file__))

app = Flask(
        __name__,
        template_folder=os.path.join(caminho_diretorio,"..", "Templates"),
        static_folder=os.path.join(caminho_diretorio,"..", "Static")
    )

origem_pastas = os.path.join(caminho_diretorio,"..","Upload")
extensoes_permitidas = {"txt","pdf"}

app.config["UPLOAD_PASTA"] = origem_pastas

# Se não tiver a pasta de uploads, criamos ela
if not os.path.exists(origem_pastas):
    os.makedirs(origem_pastas)


def entrada_arquivo(filename):
    return "." in filename and filename.rsplit(".",1)[1].lower() in extensoes_permitidas

def limpar_texto(texto):
    # Colocar texto em minusculo, remover caracteres especiais e espaços
    texto = texto.lower()
    texto = re.sub(r"[^a-zA-Z0-9\s]", "", texto)
    texto = re.sub(r"\s+", " ", texto)
    return texto.strip()

def classificar_email(texto):
    # Classificar o email por palavras-chave

    palavras_produtivas = ["solicitação", "urgente", "importante", "ação necessária", "responder", "pendente", "prioridade", "atendimento", "suporte", "assistência","pedido","reunião","agendamento","confirmação","urgente","prioridade","aprovação","encaminhamento","contrato","falha","erro","problema","reclamação","dúvida","informação","detalhes","documento","anexo","proposta","orçamento","fatura","pagamento","cobrança","relatório","análise","feedback","sugestão","melhoria","planejamento","estratégia","objetivo","meta","resultado","desempenho","avaliação","comunicação","notificação","alerta","atualização","novidade","lançamento","evento","convite","participação"]

    palavras_improdutivas = ["promoções","Aproveite","Imóveis","Descontos","Oferta","Compre agora","Grátis","Clique aqui","Inscreva-se","Ganhe","Brinde","Cupom","Sorteio","Concursos","Publicidade","Marketing","Newsletter","Boletim","Anúncio","Divulgação","Campanha","Venda","Liquidação","Promoção especial","Oferta limitada","Desconto exclusivo","Economize agora","Oferta imperdível","Compre já","Frete grátis","Garantia de satisfação","Teste grátis","Demonstração gratuita","Amostra grátis"]

    produtivas_contador = sum(1 for p in palavras_produtivas if p in texto)
    improdutivos_contador = sum(1 for p in palavras_improdutivas if p in texto)

    if improdutivos_contador > produtivas_contador:
        return "Email Não Produtivo"
    return "Email Produtivo"

def resposta_sugerida(categoria):
    # Gerar resposta baseada na classificação(classificar_email())
    if categoria == "Email Produtivo":
        return (
            "Olá!\n\n"
            "Recebemos seu email e nossa equipe já está analisando sua solicitação. "
            "Entraremos em contato com uma atualização o mais breve possível.\n\n"
            "Atenciosamente,\nEquipe de Suporte"
        )

    return(
            "Olá!\n\n"
            "Agradecemos sua mensagem! Ficamos felizes em receber seu contato. "
            "Não é necessária nenhuma ação adicional.\n\n"
            "Atenciosamente,\nEquipe de Suporte"
        )
    
def ler_arquivo_pdf(caminho_arquivo):
    # Ler arquivo PDF ou TXT e retornar o texto
    ext = caminho_arquivo.rsplit(".",1)[1].lower()

    if ext == "txt":
        with open(caminho_arquivo, "r", encoding="utf-8") as file:
            return file.read()
    
    elif ext == "pdf":
        text = ""
        with open(caminho_arquivo, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() or ""
            return text
    
    return ""

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analisar_email():
    email_text = request.form.get("emailText", "")
    email_file = request.files.get("emailFile")
    content = ""

    # Se houver arquivo válido, ler o conteúdo
    if email_file and entrada_arquivo(email_file.filename):
        filename = secure_filename(email_file.filename)
        caminho_arquivo = os.path.join(app.config["UPLOAD_PASTA"], filename)
        email_file.save(caminho_arquivo)
        content += ler_arquivo_pdf(caminho_arquivo)

    # Adicionar texto do formulário, se houver
    if email_text.strip():
        content += " " + email_text

    # Se não houver conteúdo, retorna erro
    if not content.strip():
        return jsonify({"error": "Nenhum conteúdo encontrado."}), 400

    # Processamento do texto
    processamento_texto = limpar_texto(content)
    categoria = classificar_email(processamento_texto)
    resposta = resposta_sugerida(categoria)

    return jsonify({
        "category": categoria,
        "reply": resposta
    })



# Rodar o app
if __name__ == "__main__":
    app.run(debug=True)