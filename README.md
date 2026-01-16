# Categorizador Inteligente de Emails

Este projeto é uma aplicação web para **classificação automática de emails corporativos** em **Produtivos** ou **Improdutivos**, utilizando uma **arquitetura híbrida de Inteligência Artificial (NLP)** com foco em **baixo custo operacional**, **previsibilidade** e **uso responsável de IA**, atendendo a cenários reais de produção.

A solução foi desenhada considerando **restrições de infraestrutura (512MB de RAM)** e **alto volume de mensagens**, evitando dependência de APIs pagas e garantindo escalabilidade controlada.

---

## 🎯 Objetivo do Projeto

Automatizar a leitura, classificação e sugestão de resposta para emails corporativos, reduzindo esforço humano, tempo de resposta e ruído operacional, sem comprometer compliance, segurança da informação e padronização corporativa.

---

## 🧠 Estratégia de Classificação (Diferencial do Projeto)

A aplicação utiliza uma **abordagem híbrida em três camadas**, combinando regras semânticas explícitas com **Processamento de Linguagem Natural (NLP)** baseado em **Transformers**, garantindo equilíbrio entre desempenho, custo e precisão.

### 1️⃣ Regras Explícitas de Improdutividade

Identificação direta de mensagens sem valor operacional, como:

* Spam
* Marketing
* Promoções
* Newsletters
* Mensagens sociais sem ação requerida

Essa camada garante **baixo custo computacional** e alta precisão em cenários previsíveis.

---

### 2️⃣ Regras de Intenção Produtiva

Detecta automaticamente emails que exigem ação, utilizando análise semântica por palavras-chave contextualizadas, como:

* Solicitações
* Aprovações
* Prazos
* Erros
* Documentos
* Processos internos

Essa etapa reduz dependência direta da IA e melhora a eficiência do sistema.

---

### 3️⃣ NLP com Transformer (Hugging Face – DistilBERT)

Um modelo de linguagem baseado em **Transformer (DistilBERT)** é utilizado como **camada de decisão semântica**, sendo acionado **apenas quando as regras não são suficientes** para uma classificação segura.

O modelo analisa o **contexto completo do email**, indo além de palavras-chave, permitindo identificar:

* Solicitações implícitas
* Comunicações formais
* Emails com intenção real de ação

#### Ajustes aplicados ao uso da IA:

* Limite de caracteres por requisição
* Normalização e limpeza do texto
* Uso controlado apenas como camada de desempate

Essa estratégia demonstra **uso consciente e eficaz de IA**, equilibrando precisão, custo e desempenho, atendendo aos critérios de avaliação do desafio.

---

## ✉️ Geração de Resposta Assistida por IA

Após a classificação, o sistema gera uma **resposta sugerida padronizada**, seguindo **templates corporativos pré-definidos**.

A IA é utilizada de forma **controlada** para:

* Identificar o nome do remetente
* Identificar o assunto principal do email
* Ajustar variáveis do template conforme o contexto

📌 **Importante:**

* A IA **não gera textos livres**
* Evita respostas fora do padrão corporativo
* Garante compliance e previsibilidade

Essa decisão arquitetural previne riscos comuns em soluções baseadas exclusivamente em geração de texto por IA.

---

## 🗂 Estrutura de Pastas

```
Categorizador-Inteligente-de-Emails/
│
├── Backend/
│   └── main.py          # Backend Flask e lógica de NLP
│
├── Static/
│   ├── CSS/
│   │   └── style.css    # Estilos da aplicação
│   └── JS/
│       └── main.js      # Comunicação frontend-backend
│
├── Templates/
│   └── index.html       # Interface web
│
├── Upload/              # Armazenamento temporário de arquivos
│
├── venv/                # Ambiente virtual
├── .gitignore
├── README.md
└── requirements.txt
```

---

## ⚙️ Tecnologias Utilizadas

* **Python 3**
* **Flask**
* **JavaScript / HTML / CSS**
* **PyPDF2** (leitura de PDFs)
* **Hugging Face Transformers (DistilBERT)**

---

## 🔐 Configuração do Token Hugging Face

1. Criar a variável de ambiente `HF_TOKEN`

### Windows (PowerShell)

```bash
setx HF_TOKEN "seu_token_aqui"
```

### Linux / macOS (bash/zsh)

```bash
export HF_TOKEN="seu_token_aqui"
```

No Render ou outro provedor de hospedagem, adicionar `HF_TOKEN` nas variáveis de ambiente.

---

## ▶️ Configuração e Execução

```bash
1. Clonar o repositório:

git clone https://github.com/KaykeRagoso/Categorizador-Inteligente-de-Emails
cd Categorizador_inteligente-de-Emails

2. Criar e ativar o ambiente virtual:

# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python -m venv venv
source venv/bin/activate

3. Instalar dependências:

pip install -r requirements.txt

4. Executar o backend:

python Backend/main.py

5. Acessar:

http://127.0.0.1:5000/
```

---

## 🧪 Uso da Aplicação

1. Insira o conteúdo do email no campo de texto **ou** faça upload de um arquivo (.txt ou .pdf)
2. Clique em **Analisar Email**
3. O sistema retornará:

   * Categoria do email
   * Resposta sugerida

---

## 📦 Limite de Upload

* Limite configurado: **5MB**
* Arquivos acima desse tamanho retornam erro controlado:

```json
{"error": "Arquivo muito grande. O tamanho máximo permitido é 5MB."}
```

---

## 👤 Autor

**Kayke Ragoso**
Desenvolvedor Fullstack
Projeto desenvolvido como case técnico e de portfólio, com foco em arquitetura backend, NLP aplicado e uso responsável de Inteligência Artificial.

---

✅ Projeto desenvolvido com foco em **arquitetura real**, **uso responsável de IA** e **pronto para produção**.
