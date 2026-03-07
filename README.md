# RAG Assistant – Retrieval Augmented Generation System

## Overview

The **RAG Assistant** is an intelligent question-answering system that retrieves relevant information from a knowledge base and generates accurate responses using Large Language Models (LLMs).

Unlike traditional chatbots that rely only on pre-trained knowledge, this system combines **document retrieval** with **language generation** to produce **context-aware and fact-grounded answers**.

The assistant is designed to answer user queries based on **custom documents or knowledge bases**, making it useful for:

- Institutional assistants
- Document search systems
- Knowledge base Q&A
- Enterprise document assistants

---
## Core Technologies

The system is built using a modern **Retrieval-Augmented Generation (RAG)** architecture.

### Large Language Model
- **Model:** `llama-3.3-70b-versatile`
- Used for **reasoning and answer generation** based on retrieved document context.

### Embedding Model
- **Model:** `BAAI/bge-base-en-v1.5`
- Converts documents and queries into **vector representations** for semantic search.

### Vector Database
- **Database:** **ChromaDB**
- Stores document embeddings and enables **efficient vector similarity retrieval**.

### Retrieval Strategy
The system uses **Hybrid Retrieval**, which combines:

- **Vector Similarity Search** (semantic understanding)
- **BM25 Keyword Search** (exact keyword matching)

This hybrid approach improves retrieval performance by capturing both **semantic meaning** and **exact keyword matches**.

### Reranking
After retrieval, the candidate documents are **reranked** using a **reranking model** to ensure the most relevant documents are placed at the top before being passed to the LLM.

Reranking helps improve:

- Context quality
- Retrieval precision
- Final answer accuracy

---


## Features

- Retrieval-Augmented Generation (RAG)
- Hybrid Document Retrieval
- Document Reranking
- Document relevance grading
- Hallucination detection
- Web search fallback when internal knowledge is insufficient
- Modular pipeline using LangGraph
- FastAPI backend for scalable deployment
- Hybrid Document Retrieval

---

## System Architecture

The system follows a **Retrieval-Augmented Generation pipeline** where documents are retrieved first and then used by an LLM to generate answers.

### RAG Pipeline Diagram

```mermaid
flowchart TD

A[User Query] --> B[Retrieve Documents]

B --> C[Document Relevance Grader]

C --> D{Relevant Documents?}

D -->|Yes| E[Generate Answer using LLM]

D -->|No| F[Web Search]

F --> E

E --> G[Hallucination Check]

G --> H[Final Answer Returned to User]
```
---









