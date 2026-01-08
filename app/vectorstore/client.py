from langchain_community.vectorstores import Chroma
from app.rag.embeddings import embedding_model
from app.core.config import VECTOR_DB_PATH

def get_vectorstore():
    return Chroma(
        collection_name="rag_knowledge_base",
        embedding_function=embedding_model,
        persist_directory=VECTOR_DB_PATH
    )
