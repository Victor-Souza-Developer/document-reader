
import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


def load_language_model():
    load_dotenv()

    api_key = os.getenv("GOOGLE_API_KEY", "").strip()
    model_name = os.getenv("GEMINI_MODEL", "").strip()

    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY não configurada. "
            "Adicione a chave ao arquivo .env."
        )

    if not model_name:
        raise ValueError(
            "GEMINI_MODEL não configurado. "
            "Adicione o nome do modelo ao arquivo .env."
        )

    try:
        return ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=api_key
        )
    except Exception as error:
        raise RuntimeError(
            "Não foi possível inicializar o modelo de linguagem."
        ) from error
