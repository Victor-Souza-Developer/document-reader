
from langchain_chroma import Chroma


def create_vector_store(chunks, embedding_model, persist_directory):

    vector_store = Chroma(
        collection_name="documentos_app",
        embedding_function=embedding_model,
        persist_directory=str(persist_directory)
    )

    ids = [
        f"{chunk.metadata['source']}::{chunk.metadata['chunk_index']}"
        for chunk in chunks
    ]

    vector_store.add_documents(
        documents=chunks,
        ids=ids
    )

    return vector_store
