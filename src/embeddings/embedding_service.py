from langchain_huggingface import HuggingFaceEmbeddings

def create_embeddings_model():

    embeddings_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    return embeddings_model

def generate_embeddings(chunks, embeddings_model):
    
    texts = [chunk.page_content for chunk in chunks]
    embeddings = embeddings_model.embed_documents(texts)
    
    return embeddings
