
from pathlib import Path

from src.loaders.document_loader import prepare_documents
from src.embeddings.embedding_service import load_embedding_model
from src.vectorstore.chroma_service import build_vector_index
from src.llm.llm_service import load_language_model
from src.services.rag_service import answer_question


BASE_DIR = Path(__file__).resolve().parent.parent

DOCUMENTS_DIR = BASE_DIR / "documents"
CHROMA_DIR = BASE_DIR / "chroma_db"


def build_document_index():

    DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)

    # Carrega os documentos
    document_chunks, errors = prepare_documents(DOCUMENTS_DIR)

    # Inicializa embeddings
    embedding_model = load_embedding_model()

    # Cria ou atualiza o banco vetorial
    vector_store = build_vector_index(
        document_chunks,
        embedding_model,
        CHROMA_DIR
    )

    return vector_store, errors


def initialize_services():

    # Prepara a base de conhecimento
    vector_store, errors = build_document_index()

    # Inicializa o LLM
    llm = load_language_model()

    return vector_store, llm, errors


def ask_question(vector_store, llm, question):

    # Delega a execução do RAG
    return answer_question(
        vector_store,
        llm,
        question
    )
