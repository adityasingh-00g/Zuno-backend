## RAG Pipeline Diagram

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
