from typing_extensions import TypedDict
from typing import List
from langchain_core.documents import Document
from langgraph.graph import END, StateGraph
from app.rag.webSearch import web_search
from app.rag.retriever import retrieve
from app.rag.documentGrader import grade_documents
from app.rag.generator import generate
from app.rag.decideGenerate import decide_to_generate
from app.rag.gradeGenerationhallucinationAnswer import grade_hallucination_generation_answer

class GraphState(TypedDict):
    question: str
    user_id:int
    generation: str
    web_search: str
    documents: List[Document]

def pipeline(GraphState):
    workflow = StateGraph(GraphState)

    # Add Nodes
    workflow.add_node("retrieve", retrieve)
    workflow.add_node("grade_documents", grade_documents)
    workflow.add_node("websearch", web_search)
    workflow.add_node("generate", generate)

    # Set the entry point directly to document retrieval
    workflow.set_entry_point("retrieve")  # <-- changed from route_question

    # Connect nodes
    workflow.add_edge("retrieve", "grade_documents")
    
    workflow.add_conditional_edges(
        "grade_documents",
        decide_to_generate,
        {
            "websearch": "websearch",
            "generate": "generate"
        }
    )

    workflow.add_edge("websearch", "generate")

    workflow.add_conditional_edges(
        "generate",
        grade_hallucination_generation_answer,
        {
            "not useful": "websearch",
            "useful": END
        }
    )

    app = workflow.compile()
    return app
