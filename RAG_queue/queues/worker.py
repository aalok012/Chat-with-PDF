from dotenv import load_dotenv
from openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

load_dotenv()
openai_client= OpenAI()


embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large"
)
vector_db = QdrantVectorStore.from_existing_collection(
     url = "http://localhost:6333",
     collection_name="RAG",
     embedding=embedding_model
)

# #take the user input
# query = input("ASK something: ")

def process_query(query:str):
    print("Searching chunks", query)
    search_results = vector_db.similarity_search(query=query)
    
    context="\n\n\n".join([f"Page content: {result.page_content}\nPage Number:{result.metadata['page_label']} \nFile Location: {result.metadata['source']}" for result in search_results])

    SYSTEM_PROMPT=f"""" 
    You are  a helpful AI Assistant who answers user query based on the available context
    retrieved from a PDF File along with page_content and page number.

    You should only answer the user based on the following context and navigate the 
    user to open the right page number to know more

    context:
    {context}
    """

    response= openai_client.chat.completions.create(
        model="gpt-5",
        messages=[
            {"role": "system", "content":SYSTEM_PROMPT},
            {"role": "system", "content":query },
            
        ]
    )

    print(f"🤖: {response.choices[0].message.content}" )
    return response.choices[0].message.content
#we have returned the processor function successfully 