# HR RAG Telegram Bot

Production-oriented HR Retrieval-Augmented Generation (RAG) chatbot built with Python, LangChain, Chroma, and Telegram. The system enables HR employees to search internal company documents, retrieve relevant policies, answer HR questions with citations, and gracefully refuse when the requested information is unavailable.

---

## Features

- Multi-document Retrieval-Augmented Generation (RAG)
- Telegram bot interface
- Local CLI interface
- Persistent Chroma vector database
- DOCX, PDF, and XLSX document ingestion
- Automatic document chunking
- Metadata-aware retrieval
- Source citations
- Query reformulation for follow-up questions
- Conversation memory per user
- Intent routing
- Access-level filtering
- Structured logging
- Retrieval evaluation suite
- Unit tests with Pytest
- Provider abstraction (Gemini/OpenAI ready)

---

## Current Architecture

```text
                User
                  │
        ┌─────────┴─────────┐
        │                   │
    Telegram             CLI
        │                   │
        └─────────┬─────────┘
                  │
             QA Service
                  │
          Intent Detection
                  │
        Conversation Memory
                  │
         Query Reformulation
                  │
             Retriever
                  │
        Chroma Vector Store
                  │
          Retrieved Chunks
                  │
           Prompt Builder
                  │
              LLM Provider
                  │
         Grounded Response
                  │
      Citations + Refusal Logic
```

---

## Repository Structure

```text
hr-rag-telegram-bot/

app/
│
├── access/
├── config/
├── evaluation/
├── ingestion/
├── interfaces/
├── memory/
├── prompts/
├── providers/
├── retrieval/
├── schemas/
├── services/
├── utils/
└── workflows/

data/
├── raw/
├── processed/
└── evaluation/

tests/

vectorstore/

notes/

requirements.txt
README.md
.env.example
Dockerfile
docker-compose.yml
```

---

## Supported Documents

- PDF
- DOCX
- XLSX

---

## Retrieval Pipeline

1. User submits a question.
2. Intent router determines whether the question should go through the RAG pipeline.
3. Conversation history is consulted.
4. Follow-up questions are rewritten into standalone retrieval queries.
5. Query embedding is generated.
6. Chroma performs similarity search.
7. Metadata filters are applied.
8. Retrieved chunks are injected into the prompt.
9. LLM generates an answer using only retrieved context.
10. Sources are attached.
11. If insufficient evidence exists, the assistant refuses gracefully.

---

## Metadata Stored Per Chunk

Each chunk stores rich metadata including:

- document_id
- document_title
- document_type
- policy_category
- access_level
- source
- section_heading
- page
- sheet_name
- row_range
- chunk_id
- chunk_index

---

## Supported Interfaces

### Telegram

Interactive HR chatbot.

```
python -m app.interfaces.telegram_bot
```

---

### CLI

Local testing interface.

```
python -m app.interfaces.cli
```

---

## Evaluation

### Retrieval Audit

Shows retrieval scores for various queries.

```
python -m app.evaluation.retrieval_score_audit
```

---

### Retrieval Evaluation

Runs the retrieval benchmark.

```
python -m app.evaluation.evaluator
```

---

### Unit Tests

```
pytest
```

---

## Local Setup

Create the virtual environment.

```bash
python3 -m venv .venv
```

Activate it.

```bash
source .venv/bin/activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

Copy the environment file.

```bash
cp .env.example .env
```

---

## Current Project Status

## Implemented

- Repository architecture
- Configuration management
- Provider abstraction
- Chroma integration
- Document ingestion
- Metadata extraction
- Chunking
- Persistent vector database
- Retrieval pipeline
- Citation generation
- Graceful refusal
- Query reformulation
- Conversation memory
- CLI interface
- Telegram bot
- Structured logging
- Retrieval analytics
- Metadata-aware filtering
- Access control
- Retrieval evaluation
- Unit tests

---

## Planned Roadmap

### Retrieval Quality

- Hybrid search (BM25 + dense retrieval)
- Cross-encoder reranking
- Better metadata filtering
- Chunk compression
- Dynamic Top-K
- Query expansion
- Confidence scoring

### HR Workflows

- Document summarization
- Policy comparison
- Policy extraction
- Onboarding assistant
- HR email drafting
- Action item extraction

### Production

- Docker
- Docker Compose
- Railway deployment
- Admin ingestion commands
- Document management commands
- Authentication
- Monitoring
- Evaluation dataset expansion

---

## Current Technical Stack

### Language

- Python

### Frameworks

- LangChain

### Vector Database

- Chroma

### LLM Providers

- Google Gemini
- OpenAI (provider abstraction implemented)

### Embeddings

- Gemini Embeddings
- OpenAI Embeddings (supported)

### Interfaces

- Telegram
- CLI

### Testing

- Pytest

### Logging

- Python logging
- Structured analytics

---

## Current Development Status

The project has reached a functional MVP capable of:

- Ingesting real HR documents.
- Persisting embeddings in Chroma.
- Retrieving relevant HR policies.
- Answering grounded questions with citations.
- Refusing unsupported questions.
- Maintaining conversation context.
- Operating through both CLI and Telegram.
- Running retrieval benchmarks and unit tests.

The remaining work focuses on improving retrieval quality, expanding HR workflows, production deployment, and advanced search capabilities.
