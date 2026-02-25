from serpapi import GoogleSearch
from app.core.config import GOOGLE_NEWS_API
from langchain_core.prompts import PromptTemplate
from app.rag.llm import llm
from langchain_core.output_parsers import StrOutputParser
def news_engine(state):
    query=state["question"]
    params={
        "engine":"google_news_light",
        "q":query,
        "api_key":GOOGLE_NEWS_API
    }
    search=GoogleSearch(params)
    results= search.get_dict()
    news_results=results['news_results']
    return news_results

def buildNewsPrompt(news,query):
    news_text=""
    for i,news in enumerate(news,1):
        news_text+=(
            f"{i}. Title : {news["title"]}\n"
            f"   Source : {news["source"]}\n"
            f"   Date : {news["date"]}\n"
            f"   Summary : {news["snippet"]}\n"
            f"   Link : {news["link"]}\n"
        )
    
    news_prompt = PromptTemplate(
        template="""
        <|begin_of_text|><|start_header_id|>system<|end_header_id|>
        You are a news assistant.
        Answer the user's query ONLY using the provided news articles.
        Always include the news article's link, source and data whenever you mention or cite a news item.

        <|eot_id|>

        <|start_header_id|>user<|end_header_id|>
        News Articles:
        {news}

        User Question:
        {query}

        Answer:
        <|eot_id|>

        <|start_header_id|>assistant<|end_header_id|>
        """,
        input_variables=["news", "query"]
    )
    return news_prompt,news_text


def generateNews(news,state):
    query=state["question"]
    prompt,news=buildNewsPrompt(news,query)
    newsGenerator=prompt | llm | StrOutputParser()
    newsResponse=newsGenerator.invoke({"news":news,"query":query})
    return newsResponse
