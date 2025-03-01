from langchain.chat_models import init_chat_model
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD")
uri = f"mongodb+srv://ssrir5:{MONGODB_PASSWORD}@hackcluster.vn2l2.mongodb.net/?retryWrites=true&w=majority&appName=HackCluster"
client = MongoClient(uri, server_api=ServerApi('1'))
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# client.coll

llm = init_chat_model("gpt-4o-mini", model_provider="openai")
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")



file_path = "../eosdatacontext.txt"
with open(file_path, 'r') as file:
    data = file.read()

docs = [{"page_content": data, "metadata": {}}]

print(len(docs))
print(f"{docs[0]['page_content']}\n")
print(docs[0]['metadata'])
# vector_store = MongoDBAtlasVectorSearch(
#     embedding=embeddings,
#     collection=MONGODB_COLLECTION,
#     index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
#     relevance_score_fn="cosine",
# )


