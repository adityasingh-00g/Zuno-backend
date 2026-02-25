from dotenv import load_dotenv
import os
load_dotenv()

GROQ_API_KEY=os.getenv("GROQ_API_KEY")
TAVILY_API_KEY=os.getenv("TAVILY_API_KEY")
GOOGLE_NEWS_API=os.getenv("GOOGLE_NEWS_API")
DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
CHROMA_PATH = os.getenv("CHROMA_PATH", "./chroma")
VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH")
