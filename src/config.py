import os
from dotenv import load_dotenv
# loading the env file
load_dotenv() 

class Config:
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    GOOGLE_CSE_ID = os.getenv('GOOGLE_CSE_ID')
    LANGCHAIN_API_KEY=os.getenv('LANGCHAIN_API_KEY')
    LANGCHAIN_TRACING_V2=os.getenv('LANGCHAIN_TRACING_V2') or "true"
    SERPER_API_KEY=os.getenv('SERPER_API_KEY')
    OPENAI_API_KEY=os.getenv('OPENAI_API_KEY')
    MODEL_NAME = os.getenv('MODEL_NAME')
    DATABSE_URL = os.getenv('DATABASE_URL')
    TAVILY_API_KEY = os.getenv('TAVILY_API_KEY')
    REDIS_URL = os.getenv("REDIS_URL")
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_INDEX_NAME = "colabi_pinecone"
    AGENTOPS_API_KEY = os.getenv("AGENTOPS_API_KEY")
    MONGODB_URL=os.getenv("MONGODB_URL")
    MONGODB_DB_NAME=os.getenv("MONGODB_DB_NAME")
    MONGODB_COLLECTION_NAME=os.getenv("MONGODB_COLLECTION_NAME")
