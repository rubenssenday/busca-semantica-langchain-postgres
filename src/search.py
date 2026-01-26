import os
from dotenv import load_dotenv
from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

connection = f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
collection_name = "documents"

vectorstore = PGVector(
    embeddings=embeddings,
    collection_name=collection_name,
    connection=connection,
    use_jsonb=True,
)

def search(query):
    return vectorstore.similarity_search_with_score(query, k=10)