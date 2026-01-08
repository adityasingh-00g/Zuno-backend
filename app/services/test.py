from app.services.ingestion import ingestionPipeline
from app.rag.embeddings import embedding_model
from app.rag.pipeline import GraphState,pipeline
from app.rag.retriever import retrieve
from app.rag.questionRouter import route_question

from langchain_community.embeddings import FastEmbedEmbeddings
import os

MODEL_LOCAL_PATH = "models"

FastEmbedEmbeddings(
    model_name="BAAI/bge-base-en-v1.5",
    cache_dir=MODEL_LOCAL_PATH
)


