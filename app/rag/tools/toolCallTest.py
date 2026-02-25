from app.rag.tools.toolClassifier import tool_classifier
from app.rag.tools.newsEngine import news_engine,generateNews

question="Give me news headlines of today about cricket."
state={"question":question}
#toolClassifierResponse=tool_classifier(state)
newsEngineResponse=news_engine(state)
newsResponse=generateNews(newsEngineResponse,state)
print("Question : ",question)
print("Response : ",newsResponse)
