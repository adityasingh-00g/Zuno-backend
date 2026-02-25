from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from app.rag.llm import llm

def grade_documents(state):
    question=state["question"]
    documents=state["documents"]
    filtered_docs=[]
    web_search="No"
    
    prompt = PromptTemplate(
        template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
        You are a relevance grader.

        A document is relevant if:
        - It contains the exact answer, OR
        - It contains related roles, titles, departments, or contextual information
        that can reasonably answer the question.

        Even partial matches or inferred relationships count as relevant.

        Return ONLY a valid JSON object with a single key "score".
        The value must be either "yes" or "no".
        Do not include any explanation.
        <|eot_id|>

        <|start_header_id|>user<|end_header_id|>
        Document:
        {document}

        Question:
        {question}
        <|eot_id|>

        <|start_header_id|>assistant<|end_header_id|>
        """,
            input_variables=["question", "document"],
    )

    retriever_grader=prompt | llm | JsonOutputParser()
    for doc in documents:
        score=retriever_grader.invoke({"question":question,"document":doc.page_content})
        grade=score["score"]
        if(grade.lower() == "yes"):
            filtered_docs.append(doc)
        else:
            web_search="Yes"
    
    return {"documents":filtered_docs,"question":question,"web_search":web_search}