from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from app.rag.llm import llm
def route_question(state):
    question=state["question"]
    prompt = PromptTemplate(
        template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
        You are an expert routing agent for an AI assistant designed for IIT Palakkad.

        Your task is to decide whether a user's question should be answered using one of the following data sources:
        1. **vectorstore**
        → When the question is related to IIT Palakkad (IITPKD)-specific internal information, including but not limited to:
        academics, rules, notices, hostel, mess, fees, scholarships, faculty, departments and centres, post graduate and research,
        clubs, placements, internships, administration, student affairs, technical affairs, Students Code of Ethics and Honour,
        institute clinic, sports affairs, contacts, cultural affairs, or any official institute documents (PDFs, links, circulars).

        2. **websearch**
        → For all other general, external, or up-to-date information not specific to IIT Palakkad.

        You do NOT need exact keyword matches. Use semantic understanding.

        Return a JSON object with a single key **"datasource"** and value either:
        - "vectorstore"
        - "websearch"

        No explanation. No extra text.

        Question to route: {question}
        <|eot_id|><|start_header_id|>assistant<|end_header_id|>
        """,
        input_variables=["question"]
    )

    question_router=prompt | llm | JsonOutputParser()
    source=question_router.invoke({"question":question})
    if(source["datasource"] == "websearch"):
        return "websearch"
    elif(source["datasource"] == "vectorstore"):
        return "vectorstore"