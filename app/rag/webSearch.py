import os
from langchain_community.tools.tavily_search import TavilySearchResults
from app.core.config import TAVILY_API_KEY
from langchain_core.documents import Document

def web_search(state):
    question=state["question"]
    documents=state.get("documents",[])
    web_search_tool=TavilySearchResults(
        k=2,
        tavily_api_key=TAVILY_API_KEY
    )
    docs=web_search_tool.invoke(question)
    results=[]
    for doc in docs:
        text=""
        for key,value in doc.items():
            text+=f"{key} : {value}\n"
        results.append(text)
    web_results="\n".join(text for text in results)
    #for doc in docs:
    #    for key,value in doc.items():
    #        web_results
            
    #web_results="\n".join(d["content"] for d in docs)
    web_results=Document(page_content=web_results)

    if documents is not None:
        documents.append(web_results)
    else:
        documents=[web_results]
    
    print("Web search results : ",documents)
    return {"documents":documents,"question":question}
