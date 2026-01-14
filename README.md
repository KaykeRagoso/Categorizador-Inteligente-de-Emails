Desafio AutoU - Classificador de Emails

Este projeto é uma aplicação web que classifica emails como produtivos ou improdutivos utilizando análise de palavras-chave. Ele permite enviar emails via textarea ou upload de arquivos (.txt ou .pdf), e gera uma resposta sugerida baseada na classificação.

Estrutura de Pastas
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



Funcionalidades

Classificação automática de emails em:

Email Produtivo

Email Não Produtivo

Aceita texto direto ou upload de arquivos (.txt e .pdf)

Geração de resposta sugerida baseada na classificação

Limite de upload de arquivos configurável (ex: 7 MB)

Interface web simples, com feedback de carregamento e resultados

Tecnologias Utilizadas

Python 3 + Flask (backend)

JavaScript (frontend)

HTML/CSS (interface)

PyPDF2 (leitura de PDFs)

Configuração e Execução

Clonar o repositório:

git clone <URL_DO_REPOSITORIO>
cd Desafio-AutoU-Email


Criar e ativar o ambiente virtual:

python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate


Instalar dependências:

pip install -r requirements.txt


Rodar a aplicação:

python Backend/main.py


Acesse a aplicação em:

http://127.0.0.1:5000/

Uso

Digite o conteúdo do email na textarea ou faça o upload de um arquivo.

Clique em "Analisar Email".

O resultado será exibido com:

Categoria do email

Resposta sugerida

Limite de Upload

O tamanho máximo de arquivos enviados é 7 MB (configurável no main.py com MAX_CONTENT_LENGTH).

Se excedido, o sistema retornará uma mensagem de erro amigável:

{
    "error": "Arquivo muito grande. O tamanho máximo permitido é 7 MB."
}

Melhorias Futuras

Melhorar a classificação utilizando machine learning.

Suporte a mais formatos de arquivo (ex: .docx).

Interface web responsiva e com histórico de análises.

Autor

Kayke Ragoso – Desenvolvedor Fullstack
Processo Seletivo AutoU