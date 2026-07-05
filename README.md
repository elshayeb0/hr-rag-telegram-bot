# HR RAG Telegram Bot

A multi-turn HR Retrieval-Augmented Generation chatbot built with Python, LangChain, Chroma, OpenAI, and Telegram.

## Objective

Help HR employees answer questions over internal company documents, summarize files, cite sources, and support HR workflows.

## MVP Scope

- Ingest PDF, DOCX, and XLSX files from `data/raw`
- Split documents into retrieval-friendly chunks
- Generate embeddings using OpenAI `text-embedding-3-small`
- Store embeddings persistently in Chroma
- Retrieve relevant chunks for user questions
- Answer using retrieved context only
- Include source citations
- Refuse gracefully when the answer is not available
- Maintain isolated conversation memory per Telegram user
- Reformulate follow-up questions using chat history
- Run locally through Telegram

## Tech Stack

- Python
- LangChain
- Chroma
- OpenAI API
- `text-embedding-3-small`
- `python-telegram-bot`
- `python-dotenv`
- Docker later
- Railway later

## Architecture

```txt
Telegram User
    ↓
Telegram Bot Layer
    ↓
Conversation Memory
    ↓
Query Reformulation
    ↓
Retriever
    ↓
Chroma Vector Store
    ↓
Retrieved HR Document Chunks
    ↓
RAG Chain
    ↓
Grounded Answer + Citations
