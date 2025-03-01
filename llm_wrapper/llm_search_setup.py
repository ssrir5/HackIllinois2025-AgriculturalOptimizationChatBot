# from langchain.chat_models import init_chat_model
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_community.document_loaders import PyPDFLoader
# from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD")
MONGODB_COLLECTION = "eosdatacontext"
uri = f"mongodb+srv://ssrir5:{MONGODB_PASSWORD}@hackcluster.vn2l2.mongodb.net/?retryWrites=true&w=majority&appName=HackCluster"
client = MongoClient(uri, server_api=ServerApi('1'))
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# client.coll

# llm = init_chat_model("gpt-4o-mini", model_provider="openai")
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")



# file_path = "../eosdatacontext.txt"
# with open(file_path, 'r') as file:
#     data = file.read()

# docs = [{"page_content": data, "metadata": {}}]

# print(len(docs))
# print(f"{docs[0]['page_content']}\n")
# print(len(docs[0]['page_content']))

# docs = [Document(page_content=data, metadata={})]
# file_path = "../eosdatacontext.txt"

#  DOCUMENT CHUNKING EXAMPLE

file_path = "../NDMIcontext.pdf"
loader = PyPDFLoader(file_path)

docs = loader.load()

# text_splitter = RecursiveCharacterTextSplitter(
#     chunk_size=1000, chunk_overlap=200, add_start_index=True
# )
# all_splits = text_splitter.split_documents(docs)

# print(len(all_splits))



vector_store = MongoDBAtlasVectorSearch(
    embedding=embeddings,
    collection=MONGODB_COLLECTION,
    index_name="embeddings",
    relevance_score_fn="cosine",
)

# print(f"Number of splits: {len(all_splits)}")
# for i, split in enumerate(all_splits[:5]):  # Print the first 5 splits for verification
#     print(f"Split {i+1}: {split.page_content[:200]}...")  # Print the first 200 characters of each split


# # Add documents to the vector store
# for split in all_splits:
#     vector_store.add_document(split.page_content, split.metadata)

# # Perform a vector search
# query = "What is NDMI?"
# query_embedding = embeddings.embed_query(query)
# results = vector_store.search(query_embedding, top_k=5)

# # Print the search results
# for i, result in enumerate(results):
#     print(f"Result {i+1}: {result['page_content'][:200]}...")  # Print the first 200 characters of each result
