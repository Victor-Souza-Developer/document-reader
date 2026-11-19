# Assistente Inteligente de Documentos | RAG

Aplicação desktop desenvolvida em Python que utiliza **Retrieval-Augmented Generation (RAG)** para consultar e relacionar informações presentes em documentos PDF.

O sistema processa os documentos, gera embeddings, armazena os vetores no ChromaDB e utiliza o Google Gemini para responder perguntas com base no conteúdo recuperado.

## Funcionalidades

- Importação e processamento de arquivos PDF.
- Extração e divisão de texto em chunks.
- Geração local de embeddings.
- Armazenamento vetorial com ChromaDB.
- Busca semântica entre diferentes documentos.
- Geração de respostas com Google Gemini.
- Identificação das fontes utilizadas nas respostas.
- Interface desktop desenvolvida com PySide6.

## Arquitetura

A aplicação utiliza uma arquitetura modular, separando interface, processamento de documentos, embeddings, armazenamento vetorial, prompts e serviços de consulta.

![Arquitetura do projeto](./docs/arquitetura.png)

## Tecnologias

- Python
- PySide6
- LangChain
- Hugging Face / Sentence Transformers
- ChromaDB
- Google Gemini
- PyPDF

## Execução

Clone o repositório:

```bash
git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
cd SEU_REPOSITORIO
```

Crie e ative o ambiente virtual:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Configure o arquivo `.env` na raiz:

```env
GOOGLE_API_KEY=SUA_CHAVE_API
GEMINI_MODEL=gemini-3.5-flash-lite
```

Inicie a aplicação:

```bash
python main.py
```

## Organização

- `src/loaders/`: extração e divisão dos documentos.
- `src/embeddings/`: geração de embeddings.
- `src/vectorstore/`: integração com ChromaDB.
- `src/llm/`: inicialização do Gemini.
- `src/prompts/`: instruções utilizadas pelo RAG.
- `src/services/`: recuperação de contexto e geração de respostas.
- `src/ui/`: interface desktop.
- `src/caller.py`: orquestração dos componentes.

## Observação

Projeto desenvolvido para estudo e aplicação prática de RAG, busca semântica, embeddings e integração com modelos de linguagem.
