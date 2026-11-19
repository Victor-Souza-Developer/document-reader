
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def prepare_documents(documents_dir):

    pdf_files = sorted(Path(documents_dir).glob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError("Nenhum documento PDF encontrado.")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    all_chunks = []
    errors = []

    for pdf_file in pdf_files:

        try:
            loader = PyPDFLoader(str(pdf_file))
            documents = loader.load()

            chunks = text_splitter.split_documents(documents)

            for index, chunk in enumerate(chunks):
                chunk.metadata["source"] = pdf_file.name
                chunk.metadata["chunk_index"] = index

            all_chunks.extend(chunks)

        except Exception as error:
            errors.append(f"{pdf_file.name}: {error}")

    if not all_chunks:
        raise RuntimeError(
            "Não foi possível extrair conteúdo dos documentos."
        )

    return all_chunks, errors
