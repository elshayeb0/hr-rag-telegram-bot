from time import sleep

from app.config import settings
from app.ingestion.loaders import load_directory
from app.ingestion.splitter import split_documents
from app.retrieval.vectorstore import add_chunks
from app.schemas import DocumentChunk


def _batch_chunks(chunks: list[DocumentChunk], batch_size: int) -> list[list[DocumentChunk]]:
    return [chunks[index:index + batch_size] for index in range(0, len(chunks), batch_size)]


def ingest_documents() -> list[DocumentChunk]:
    raw_documents = load_directory(settings.raw_data_dir)
    chunks = split_documents(raw_documents)

    batches = _batch_chunks(chunks, settings.ingest_batch_size)

    for index, batch in enumerate(batches, start=1):
        print(f"Ingesting batch {index}/{len(batches)} ({len(batch)} chunks)...")
        add_chunks(batch)

        if index < len(batches):
            sleep(settings.ingest_batch_delay_seconds)

    return chunks


if __name__ == "__main__":
    ingested_chunks = ingest_documents()
    print(f"Ingested {len(ingested_chunks)} chunks into Chroma.")
