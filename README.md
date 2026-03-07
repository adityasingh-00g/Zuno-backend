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

## Features

- Retrieval-Augmented Generation (RAG)
- Document relevance grading
- Hallucination detection
- Web search fallback when internal knowledge is insufficient
- Modular pipeline using LangGraph
- FastAPI backend for scalable deployment

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

---

## Workflow

1. User submits a query.
2. System retrieves relevant documents from the knowledge base.
3. Retrieved documents are graded for relevance.
4. If documents are sufficient, the system generates an answer.
5. If documents are insufficient, the system performs web search.
6. LLM generates the final response using retrieved context.
7. Generated answer is checked for hallucinations.

---

## Project Structure



