from groq import Groq
from langchain_groq import ChatGroq
from app.core.config import GROQ_API_KEY
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.rag.llm import llm

def generate(state):
    question=state["question"]
    documents=state["documents"]
    context="\n\n".join(doc.page_content for doc in documents)
    prompt=PromptTemplate(
        template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|> You are an assistant for question-answering tasks. 
        Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. 
        Provide a clear and detailed answer based on the context. <|eot_id|><|start_header_id|>user<|end_header_id|>
        Question: {question} 
        Context: {context} 
        Answer: <|eot_id|><|start_header_id|>assistant<|end_header_id|>""",
        input_variables=["question", "context"],
    )
    llm_chain=prompt | llm | StrOutputParser()
    generation=llm_chain.invoke({"question":question,"context":context})
    print("llm Generated response : ",generation)
    return {"documents":documents,"question":question,"generation":generation}
    
