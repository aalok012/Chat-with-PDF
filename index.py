from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
pdf_path = Path(__file__).parent / "plato.pdf"

load_dotenv()

#load this file in python program
loader = PyPDFLoader(pdf_path)
docs= loader.load()

#spilt the docs into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=400 
        
)
chunks= text_splitter.split_documents(documents=docs)

#next step is to create vector embeddings from the chunk

#vector embeddings
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

#now the vector embedding created above for the chunks and should be stored in the qdrant db

vector_store = QdrantVectorStore.from_documents(
    documents= chunks,
    embedding = embedding_model,
    url = "http://localhost:6333", 
    collection_name ="RAG"
    
    
)
print("Indexing of documents")
 
