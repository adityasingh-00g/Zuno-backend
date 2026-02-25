from sentence_transformers import CrossEncoder
import numpy as np


reranker=CrossEncoder("BAAI/bge-reranker-large")

def rerank(query,retrieved_docs,top_k=5):
    pairs=[(query,doc.page_content) for doc in retrieved_docs]
    scores=reranker.predict(pairs)
    reranked_indices=np.argsort(scores)[::-1]
    reranked_docs=[retrieved_docs[i] for i in reranked_indices[:top_k]]
    return reranked_docs