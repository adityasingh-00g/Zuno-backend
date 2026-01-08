from langchain_community.embeddings.fastembed import FastEmbedEmbeddings

# Global model (loaded once per worker)
embedding_model = FastEmbedEmbeddings(
    model_name="BAAI/bge-base-en-v1.5"
)

def warmup_embeddings():
    embedding_model.embed_query("warmup")
