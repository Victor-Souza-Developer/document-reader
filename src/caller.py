
from pathlib import Path

from src.loaders.document_loader import load_and_split_documents
from src.embeddings.embedding_service import create_embeddings_model
from src.vectorstore.chroma_service import create_vector_store
from src.llm.llm_service import create_llm
from src.services.rag_service import generate_answer


BASE_DIR = Path(__file__).resolve().parent.parent

DOCUMENTS_DIR = BASE_DIR / "documents"
CHROMA_DIR = BASE_DIR / "chroma_db"


def build_knowledge_base():

    DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Carrega os documentos
    chunks, errors = load_and_split_documents(DOCUMENTS_DIR)

    # 2. Inicializa embeddings
    embedding_model = create_embeddings_model()

    # 3. Cria ou atualiza o banco vetorial
    vector_store = create_vector_store(
        chunks,
        embedding_model,
        CHROMA_DIR
    )

    return vector_store, errors


def initialize_application():

    # 1. Prepara a base de conhecimento
    vector_store, errors = build_knowledge_base()

    # 2. Inicializa o LLM
    llm = create_llm()

    return vector_store, llm, errors


def ask_question(vector_store, llm, question):

    # Delega a execução do RAG
    return generate_answer(
        vector_store,
        llm,
        question
    )
