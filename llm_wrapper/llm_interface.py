from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import os
from .prompt_retriever import PromptRetriever

class LLMInterface:
    def __init__(self, question):
        load_dotenv()
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=self.OPENAI_API_KEY)
        self.prompt_retriever = PromptRetriever(question)

    def add_context_from_file(self, file_path):
        self.prompt_retriever.add_context_from_file(file_path)

    def add_context(self, additional_context):
        self.prompt_retriever.add_context(additional_context)

    def overwrite_question(self, new_question):
        self.prompt_retriever.overwrite_question(new_question)

    def get_response(self):
        prompt = self.prompt_retriever.get_prompt()
        response = self.llm(prompt)
        return response['choices'][0]['message']['content']

# Example usage
if __name__ == "__main__":
    question = "What is the current NDMI reading indicating for irrigation planning?"
    llm_interface = LLMInterface(question)
    
    # Add context from a text file
    file_path = "../eosdatacontext.txt"
    llm_interface.add_context_from_file(file_path)
    
    # Add additional context
    additional_context = "Additional context from satellite API."
    llm_interface.add_context(additional_context)
    
    # Get the response from the OpenAI model
    response = llm_interface.get_response()
    print("Response from the chatbot:")
    print(response)