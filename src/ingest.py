from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
import os
from dotenv import load_dotenv

load_dotenv()

base = os.path.dirname(os.path.abspath(__file__))
pdf_path = os.path.join(base, "..", "document.pdf")

loader = PyPDFLoader(pdf_path)
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150, add_start_index=False)
docs = text_splitter.split_documents(documents)

if not docs:
    raise ValueError("No documents were loaded from the PDF.")

enriched = [
    Document(
        page_content=d.page_content,
        metadata={k: v for k, v in d.metadata.items() if v not in ("", None)}
    )
    for d in docs
]    

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

connection = f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
collection_name = "documents"

vectorstore = PGVector(
    embeddings=embeddings,
    collection_name=collection_name,
    connection=connection,
    use_jsonb=True,
)

vectorstore.add_documents(docs)

print("PDF ingested successfully!")