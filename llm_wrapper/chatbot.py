from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os
from uuid import uuid4


class AgriculturalOptimizationChatBot:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD")
        self.DB_NAME = "langchain_test_db"
        self.COLLECTION_NAME = "langchain_test_vectorstores"
        self.ATLAS_VECTOR_SEARCH_INDEX_NAME = "langchain-test-index-vectorstores"

        # Connect to MongoDB Atlas
        uri = f"mongodb+srv://ssrir5:{self.MONGODB_PASSWORD}@hackcluster.vn2l2.mongodb.net/?retryWrites=true&w=majority&appName=HackCluster"
        self.client = MongoClient(uri)
        try:
            self.client.admin.command("ping")
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

        # Initialize OpenAI embeddings
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

        # Load the PDF document containing agricultural data (e.g., NDMI context)
        file_path = "../NDMIcontext.pdf"
        loader = PyPDFLoader(file_path)
        docs = loader.load()

        # Split the document into smaller chunks for more granular retrieval
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200, add_start_index=True
        )
        self.doc_chunks = text_splitter.split_documents(docs)
        print(f"Total document chunks: {len(self.doc_chunks)}")

        # Initialize your MongoDB Atlas vector store
        self.MONGODB_COLLECTION = self.client[self.DB_NAME][self.COLLECTION_NAME]
        self.vector_store = MongoDBAtlasVectorSearch(
            collection=self.MONGODB_COLLECTION,
            embedding=self.embeddings,
            index_name=self.ATLAS_VECTOR_SEARCH_INDEX_NAME,
            relevance_score_fn="cosine",
        )

        # Add documents to the vector store
        uuiuds = [str(uuid4()) for _ in range(len(self.doc_chunks))]
        self.vector_store.create_vector_search_index(dimensions=1536)
        for chunk, uuid in zip(self.doc_chunks, uuiuds):
            self.vector_store.add_documents(documents=[chunk], ids=[uuid])
        print("Documents have been added to the vector store.")

        self.prompt_template = PromptTemplate(
            input_variables=["context", "question"],
            template=(
                "You are an agricultural planning optimization assistant. Your role is to help farmers make data-driven "
                "decisions to optimize crop yields and resource usage. You have access to detailed farm data including NDMI "
                "measurements, soil moisture levels, weather forecasts, and more. When providing advice, integrate insights from "
                "this data to recommend the best planting schedules, irrigation strategies, and resource allocation. If any key "
                "details are unclear, ask for more information.\n\n"
                "Context:\n{context}\n\n"
                "Question: {question}\n"
                "Answer:"
            ),
        )

        self.llm = ChatOpenAI(
            model="gpt-4o", temperature=0, openai_api_key=self.OPENAI_API_KEY
        )

        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",  # "stuff" concatenates retrieved documents for context
            retriever=self.vector_store.as_retriever(),
            chain_type_kwargs={"prompt": self.prompt_template},
        )

    def query(self, question):
        result = self.qa_chain.run(question)
        return result


# Example usage
# if __name__ == "__main__":
#     chatbot = AgriculturalOptimizationChatBot()
#     query = "What is the current NDMI reading indicating for irrigation planning?"
#     response = chatbot.query(query)
#     print("Response from the chatbot:")
#     print(response)
