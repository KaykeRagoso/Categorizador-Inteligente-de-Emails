# Desafio AutoU - Classificador de Emails

 - Este projeto é uma aplicação web para classificação automática de emails em Produtivos ou Improdutivos, utilizando uma abordagem híbrida de NLP local, combinando regras semânticas com análise de linguagem natural, sem uso de APIs pagas.

 - A aplicação permite o envio de emails via textarea ou upload de arquivos (.txt ou .pdf), processa o conteúdo localmente e retorna a classificação de forma rápida e eficiente.

--- 

### Estratégia de Classificação (Diferencial do Projeto)
 - A classificação utiliza uma lógica híbrida em três camadas:

 - Regras explícitas de improdutividade
 - Identifica mensagens sociais, spam ou sem intenção de ação
 - (ex: promoções, ofertas, mensagens de cordialidade)

 - Regras de intenção produtiva
 - Detecta palavras-chave relacionadas a ações, solicitações, prazos e processos

 - NLP Local (Hugging Face – DistilBERT)
 - Utilizado apenas como camada de desempate, evitando erros comuns de classificação por sentimento

 ### Essa abordagem reduz falsos positivos e garante classificação mais precisa, mesmo sem uso de IA paga.

## Estrutura de Pastas

Desafio-AutoU-Email/

│

├── Backend/

│   └── main.py          # Código principal do Flask

│

├── Static/

│   ├── CSS/

│   │   └── style.css    # Estilos da aplicação

│   └── JS/

│       └── main.js      # Lógica de envio do formulário e manipulação do DOM

│

├── Templates/

│   └── index.html       # Página principal com formulário de envio

│

├── Upload/

│   └── Text.txt         # Arquivos enviados para análise (armazenamento temporário)

│

├── venv/                # Ambiente virtual do Python

├── .gitattributes

├── .gitignore           # Ignora venv, uploads e arquivos temporários

├── README.md            # Este arquivo

└── requirements.txt     # Dependências do projeto

---

## Funcionalidades

- Classificação automática de emails em:

  - **Email Produtivo**

  - **Email Não Produtivo**

- Aceita texto direto ou upload de arquivos (.txt e .pdf)

- Geração de resposta sugerida baseada na classificação

- Limite de upload de arquivos configurável (ex: 7 MB)

- Interface web simples, com feedback de carregamento e resultados

---

## Tecnologias Utilizadas

- **Python 3 + Flask** (backend)

- **JavaScript** (frontend)

- **HTML/CSS** (interface)

- **PyPDF2** (leitura de PDFs)

- **Tranformers(Hugging Face) - NLP Local**

---

## Configuração e Execução
````bash
1. Clonar o repostório:

git clone <URL_DO_REPOSITORIO>
cd Desafio-AutoU-Email

2. Criar e ativar o ambiente virtual:
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate

3. Instalar dependências:

pip install -r requirements.txt

4. Rodar a aplicação:

python Backend/main.py

5. Acesse a aplicação em:

http://127.0.0.1:5000/
````
## Uso
1. Digite o conteúdo do email na textarea ou faça o upload de um arquivo.
2. Clique em "Analisar Email".
3. O resultado será exibido com:
    - Categoria do email
    - Resposta sugerida

## Limite do Upload

O tamanho máximo de arquivos enviados é 7 MB (configurável no main.py com MAX_CONTENT_LENGTH).

Se excedido, o sistema retornará uma mensagem de erro amigável:   "error": "Arquivo muito grande. O tamanho máximo permitido é 7 MB."

## Autor

Kayke Ragoso – Desenvolvedor Fullstack
Processo Seletivo AutoU