import unittest
from unittest.mock import patch

from src.services.rag_service import answer_question


class FakeChunk:
    def __init__(self, content, source="manual.pdf", page=0):
        self.page_content = content
        self.metadata = {
            "source": source,
            "page": page
        }


class FakeVectorStore:
    def __init__(self, chunks):
        self.chunks = chunks

    def similarity_search(self, question, k):
        return self.chunks[:k]


class FakePrompt:
    def invoke(self, values):
        return values


class FakeModel:
    def invoke(self, messages):
        return type("Response", (), {"content": "Resposta de teste"})()


class AnswerQuestionTests(unittest.TestCase):
    @patch("src.services.rag_service.create_rag_prompt", return_value=FakePrompt())
    def test_returns_answer_and_sources(self, _create_prompt):
        vector_store = FakeVectorStore([
            FakeChunk("Conteúdo relevante")
        ])

        answer, sources = answer_question(
            vector_store,
            FakeModel(),
            "Qual é a informação?"
        )

        self.assertEqual(answer, "Resposta de teste")
        self.assertEqual(sources, ["manual.pdf - Página 1"])

    def test_fails_when_no_chunk_is_found(self):
        vector_store = FakeVectorStore([])

        with self.assertRaises(RuntimeError):
            answer_question(vector_store, FakeModel(), "Pergunta")


if __name__ == "__main__":
    unittest.main()
