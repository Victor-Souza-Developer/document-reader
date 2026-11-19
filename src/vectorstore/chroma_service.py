
from langchain_chroma import Chroma


def build_vector_index(document_chunks, embedding_model, persist_directory):
    """Cria ou sincroniza o índice vetorial com os documentos atuais."""

    vector_store = Chroma(
        collection_name="documentos_app",
        embedding_function=embedding_model,
        persist_directory=str(persist_directory)
    )

    chunk_ids = [build_chunk_id(chunk) for chunk in document_chunks]
    current_ids = set(chunk_ids)

    stored_records = vector_store.get()
    stored_ids = set(stored_records.get("ids", []))

    stale_ids = stored_ids - current_ids
    if stale_ids:
        vector_store.delete(ids=list(stale_ids))

    if not document_chunks:
        return vector_store

    existing_records = vector_store.get(
        ids=chunk_ids,
        include=["documents"]
    )
    existing_documents = dict(
        zip(
            existing_records.get("ids", []),
            existing_records.get("documents", [])
        )
    )

    chunks_to_add = []
    ids_to_add = []
    chunks_to_update = []
    ids_to_update = []

    for chunk, chunk_id in zip(document_chunks, chunk_ids):
        stored_content = existing_documents.get(chunk_id)

        if stored_content is None:
            chunks_to_add.append(chunk)
            ids_to_add.append(chunk_id)
        elif stored_content != chunk.page_content:
            chunks_to_update.append(chunk)
            ids_to_update.append(chunk_id)

    if chunks_to_add:
        vector_store.add_documents(
            documents=chunks_to_add,
            ids=ids_to_add
        )

    if chunks_to_update:
        vector_store.update_documents(
            ids=ids_to_update,
            documents=chunks_to_update
        )

    return vector_store


def build_chunk_id(chunk):
    """Gera um ID estável para cada chunk de documento."""

    return (
        f"{chunk.metadata['source']}::"
        f"{chunk.metadata['chunk_index']}"
    )
