from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os

class SemanticSearch:
    def __init__(self):
        load_dotenv()
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD")
        self.DB_NAME = "langchain_test_db"
        self.COLLECTION_NAME = "langchain_test_vectorstores"
        self.ATLAS_VECTOR_SEARCH_INDEX_NAME = "langchain-test-index-vectorstores"

        uri = f"mongodb+srv://ssrir5:{self.MONGODB_PASSWORD}@hackcluster.vn2l2.mongodb.net/?retryWrites=true&w=majority&appName=HackCluster"
        self.client = MongoClient(uri)
        try:
            self.client.admin.command("ping")
            print("Connected to MongoDB!")
        except Exception as e:
            print(e)

        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

        self.MONGODB_COLLECTION = self.client[self.DB_NAME][self.COLLECTION_NAME]
        self.vector_store = MongoDBAtlasVectorSearch(
            collection=self.MONGODB_COLLECTION,
            embedding=self.embeddings,
            index_name=self.ATLAS_VECTOR_SEARCH_INDEX_NAME,
            relevance_score_fn="cosine",
        )

    def search(self, query):
        query_embedding = self.embeddings.embed_query(query)
        results = self.vector_store.search(query_embedding, top_k=5)
        return "\n".join([result['page_content'] for result in results])
