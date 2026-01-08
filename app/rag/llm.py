from groq import Groq
from langchain_groq import ChatGroq
from app.core.config import GROQ_API_KEY

llm = ChatGroq(
        temperature=0,
        model_name="llama-3.1-8b-instant",
        api_key=GROQ_API_KEY
    )