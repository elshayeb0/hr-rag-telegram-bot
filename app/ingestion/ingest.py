from app.config import settings
from app.ingestion.loaders import load_directory
from app.ingestion.splitter import split_documents
from app.retrieval.vectorstore import add_chunks
from app.schemas import DocumentChunk


def ingest_documents() -> list[DocumentChunk]:
    raw_documents = load_directory(settings.raw_data_dir)
    chunks = split_documents(raw_documents)
    add_chunks(chunks)
    return chunks


if __name__ == "__main__":
    ingested_chunks = ingest_documents()
    print(f"Ingested {len(ingested_chunks)} chunks into Chroma.")
