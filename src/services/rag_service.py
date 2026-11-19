
from src.prompts.rag_prompt import create_rag_prompt


def generate_answer(vector_store, llm, question):

    # 1. Recupera os trechos relevantes
    documents = vector_store.similarity_search(
        question,
        k=8
    )

    if not documents:
        raise RuntimeError("Nenhum conteúdo relevante encontrado.")

    # 2. Monta o contexto e identifica as fontes
    context_parts = []
    sources = []

    for document in documents:

        source = document.metadata.get(
            "source",
            "Documento desconhecido"
        )

        page = document.metadata.get("page", 0) + 1

        context_parts.append(
            f"Documento: {source}\n"
            f"Página: {page}\n"
            f"Conteúdo: {document.page_content}"
        )

        source_info = f"{source} - Página {page}"

        if source_info not in sources:
            sources.append(source_info)

    context = "\n\n".join(context_parts)

    # 3. Obtém o prompt
    prompt = create_rag_prompt()

    # 4. Prepara a entrada
    messages = prompt.invoke({
        "context": context,
        "question": question
    })

    # 5. Solicita a resposta ao Gemini
    response = llm.invoke(messages)

    answer = response.content

    if isinstance(answer, list):
        answer = "\n".join(
            block.get("text", "")
            if isinstance(block, dict)
            else str(block)
            for block in answer
        )

    return answer, sources
