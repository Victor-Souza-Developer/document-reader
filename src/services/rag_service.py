
from src.prompts.rag_prompt import create_rag_prompt


def answer_question(vector_store, llm, question):

    # Recupera os trechos relevantes
    retrieved_chunks = vector_store.similarity_search(
        question,
        k=8
    )

    if not retrieved_chunks:
        raise RuntimeError("Nenhum conteúdo relevante encontrado.")

    # Monta o contexto e identifica as fontes
    context_sections = []
    sources = []

    for chunk in retrieved_chunks:

        source = chunk.metadata.get(
            "source",
            "Documento desconhecido"
        )

        page = chunk.metadata.get("page", 0) + 1

        context_sections.append(
            f"Documento: {source}\n"
            f"Página: {page}\n"
            f"Conteúdo: {chunk.page_content}"
        )

        source_info = f"{source} - Página {page}"

        if source_info not in sources:
            sources.append(source_info)

    context = "\n\n".join(context_sections)

    # Verifica o prompt
    prompt = create_rag_prompt()

    # 4. Prepara a entrada
    messages = prompt.invoke({
        "context": context,
        "question": question
    })

    # Faz a requisição ao Gemini
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
