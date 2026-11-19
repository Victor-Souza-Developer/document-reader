
import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


def create_llm():

    load_dotenv()

    api_key = os.getenv("GOOGLE_API_KEY")
    model_name = os.getenv("GEMINI_MODEL")

    if not api_key:
        raise ValueError("GOOGLE_API_KEY não encontrada no .env")

    if not model_name:
        raise ValueError("GEMINI_MODEL não configurado no .env")

    llm = ChatGoogleGenerativeAI(
        model=model_name,
        google_api_key=api_key
    )

    return llm
