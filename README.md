# Projeto de Ingestão e Busca Semântica com LangChain e Postgres

Este projeto implementa um sistema de busca semântica para documentos PDF utilizando LangChain, OpenAI Embeddings (ou Gemini Embeddings), e PostgreSQL com a extensão pgVector. O usuário pode ingerir um arquivo PDF e, em seguida, fazer perguntas via linha de comando (CLI) para receber respostas baseadas exclusivamente no conteúdo do PDF.

## Tecnologias Obrigatórias

*   **Linguagem:** Python
*   **Framework:** LangChain
*   **Banco de Dados:** PostgreSQL + pgVector
*   **Execução do Banco de Dados:** Docker & Docker Compose

## Pré-requisitos

Certifique-se de que você tem as seguintes ferramentas instaladas em sua máquina:

*   **Python 3.9+**
*   **Docker** e **Docker Compose**

## Passo a Passo para Configurar e Executar o Projeto

### 1. Configurar o Arquivo `.env`

Este arquivo conterá as variáveis de ambiente necessárias para o projeto, incluindo suas chaves de API e credenciais do banco de dados.

*   Crie uma cópia do arquivo de exemplo de variáveis de ambiente:
    ```bash
    cp .env_example .env
    ```
*   Edite o arquivo `.env` que você acabou de criar e preencha as seguintes variáveis:
    *   `OPENAI_API_KEY`: Sua chave de API da OpenAI (ou `GEMINI_API_KEY` se for usar Gemini).
    *   `POSTGRES_USER`: Nome de usuário para o PostgreSQL (sugestão: `user`).
    *   `POSTGRES_PASSWORD`: Senha para o PostgreSQL (sugestão: `password`).
    *   `POSTGRES_HOST`: Host do PostgreSQL (para Docker Compose, use o nome do serviço: `postgres_rag`).
    *   `POSTGRES_PORT`: Porta do PostgreSQL (padrão: `5432`).
    *   `POSTGRES_DB`: Nome do banco de dados PostgreSQL (sugestão: `documents`).
    *   `OPENAI_MODEL`: **Para Embeddings com OpenAI**, defina como `text-embedding-3-small`.
    *   `OPENAI_CHAT_MODEL`: **Para Chat com OpenAI**, defina como `gpt-3.5-turbo` (ou outro modelo de chat de sua preferência).
    *   `GEMINI_MODEL`: **Para Embeddings com Gemini**, defina como `models/embedding-001`.
    *   `GEMINI_CHAT_MODEL`: **Para Chat com Gemini**, defina como `gemini-2.5-flash-lite`.

    Exemplo de `.env` (preencha `YOUR_OPENAI_API_KEY` com sua chave real):
    ```ini
    OPENAI_API_KEY=YOUR_OPENAI_API_KEY
    POSTGRES_USER=user
    POSTGRES_PASSWORD=password
    POSTGRES_HOST=postgres_rag
    POSTGRES_PORT=5432
    POSTGRES_DB=documents
    OPENAI_MODEL=text-embedding-3-small
    OPENAI_CHAT_MODEL=gpt-3.5-turbo
    ```
    *   **Importante**: Se você for usar Gemini, certifique-se de definir as variáveis `GEMINI_API_KEY`, `GEMINI_MODEL` e `GEMINI_CHAT_MODEL` e ajustar os arquivos `ingest.py` e `chat.py` para usar as classes de embeddings e LLM da Gemini.

### 2. Subir o Banco de Dados com Docker Compose

Navegue até a raiz do seu projeto no terminal (onde `docker-compose.yaml` está localizado) e execute o seguinte comando:

```bash
docker-compose up -d
```

Aguarde alguns segundos para que o contêiner do PostgreSQL seja inicializado e esteja saudável. Você pode verificar o status com `docker-compose ps`.

### 3. Instalar as Dependências do Projeto

É altamente recomendável usar um ambiente virtual Python para gerenciar as dependências do projeto.

*   Crie e ative um ambiente virtual (se ainda não o fez):
    ```bash
    python -m venv venv
    # No Windows:
    .\venv\Scripts\activate
    # No macOS/Linux:
    source venv/bin/activate
    ```
*   Instale todas as dependências listadas no `src/requirements.txt`:
    ```bash
    python -m pip install -r src/requirements.txt
    ```

### 4. Executar o Arquivo `ingest.py`

Este script é responsável por carregar o documento PDF, dividi-lo em chunks, criar embeddings e armazená-los no banco de dados PostgreSQL.

*   Coloque o arquivo PDF que deseja ingerir na pasta `src/` e nomeie-o como `document.pdf`. Se o nome ou o caminho for diferente, ajuste a linha `loader = PyPDFLoader("src/document.pdf")` no `ingest.py`.
*   Execute o script de ingestão:
    ```bash
    python src/ingest.py
    ```
*   Após a execução bem-sucedida, você verá a mensagem "PDF ingested successfully!".

### 5. Executar o Arquivo `chat.py`

Este script inicia a interface de linha de comando para você interagir com o conteúdo ingerido.

*   Execute o script de chat:
    ```bash
    python src/chat.py
    ```
*   Você verá o prompt "Faça sua pergunta: ". Digite suas perguntas e pressione Enter.
*   Para sair da aplicação, digite "sair" e pressione Enter.

---

### Exemplo de Interação no CLI

```
Faça sua pergunta: Qual o faturamento da Empresa SuperTechIABrazil?
RESPOSTA: O faturamento foi de 10 milhões de reais.

Faça sua pergunta: Quantos clientes temos em 2024?
RESPOSTA: Não tenho informações necessárias para responder sua pergunta.

Faça sua pergunta: sair
```