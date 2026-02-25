from app.services.ingestion import ingestionPipeline
from app.rag.embeddings import embedding_model
from app.rag.pipeline import GraphState,pipeline
from app.rag.retriever import retrieve
from app.rag.questionRouter import route_question
from app.rag.generator import generate
from app.rag.webSearch import web_search
from app.rag.documentGrader import grade_documents
from app.rag.gradeGenerationhallucinationAnswer import grade_hallucination_generation_answer
from app.vectorstore.client import get_vectorstore
from langchain_community.embeddings import FastEmbedEmbeddings
import os

#state={"question":"Reinforcement Learning: An Introduction"}
#response=retrieve(state)
#print("Retrieved docs : ",response)
"""
# Document grader (Pass)
response=grade_documents(response)

# Web search
webSearch_response=web_search(response)

# Generator
llm_response=generate(webSearch_response)

# Answer and hallucination grader
score=grade_hallucination_generation_answer(llm_response)
print("Score : ",score)"""
vectorstore=get_vectorstore()
data=vectorstore.get()
metadatas=data["metadatas"]
sources={meta.get("source") for meta in metadatas}
print("Sources : ",sources)



