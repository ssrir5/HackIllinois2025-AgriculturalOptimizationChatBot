import openai
from dotenv import load_dotenv
import os

# from llm_wrapper.prompt_retriever import PromptRetriever


class PromptRetriever:
    def __init__(self, question):
         self.question = question
         self.context = ""
         self.prompt_template = (
            "You are an agricultural planning optimization assistant. Your role is to help farmers make data-driven "
            "decisions to optimize crop yields and resource usage. You have access to detailed farm data including NDMI "
            "measurements, soil moisture levels, weather forecasts, and more. When providing advice, integrate insights from "
            "this data to recommend the best planting schedules, irrigation strategies, and resource allocation. If any key "
            "details are unclear, ask for more information. However, you need to be extremely concise about the advice you give unless you are asked to elaborate. \n\n"
            "Example 1:\n"
            "Q: \"My NDMI is low, NDVI is high, and EVI shows early stress. What irrigation strategy should I follow?\"\n"
            "A: \"Hi there! Your data indicates that while your vegetation is healthy (high NDVI), there's some moisture stress (low NDMI) "
            "and early signs of stress (EVI). I recommend increasing targeted irrigation in the affected areas for the next week, then monitoring for improvements. "
            "Let me know if you'd like more details!\"\n\n"
            "Example 2:\n"
            "Q: \"How do I classify my farm environment based on current sensor data?\"\n"
            "A: \"Hello! Based on your sensor readings, it seems you're in a semi-arid environment—healthy vegetation overall, but with some moisture limitations. "
            "This suggests a dryland system that could benefit from occasional supplemental irrigation. If you need further insights, feel free to ask!\"\n\n"
            "Example 3:\n"
            "Q: \"Given my climate and soil moisture trends, which crops are optimal for my farm?\"\n"
            "A: \"Hi! Considering your climate data and current soil moisture levels, drought-tolerant crops like sorghum or millet would be ideal. "
            "They perform well under lower water conditions while maintaining good yields. I'm here to help if you need more crop recommendations!\"\n\n"
            "Context:\n{context}\n\n"
            "Question: {question}\n"
            "Answer:"
         )

    def add_context_from_file(self, file_path):
        with open(file_path, "r") as file:
            self.context += file.read() + "\n"

    def add_context(self, additional_context):
        self.context += additional_context + "\n"

    def overwrite_question(self, new_question):
        self.question = new_question

    def get_prompt(self):
        return self.prompt_template.format(context=self.context, question=self.question)


import os
from dotenv import load_dotenv
from openai import OpenAI

# Assume PromptRetriever is defined elsewhere
class LLMInterface:
    def __init__(self, question):
        load_dotenv()
        self.OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
        # Initialize the OpenAI client with the API key
        self.client = OpenAI(api_key=self.OPENAI_API_KEY)
        self.prompt_retriever = PromptRetriever(question)
        self.messages = [
            {"role": "system", "content": "You are a helpful assistant!"},
        ]

    def add_context_from_file(self, file_path):
        self.prompt_retriever.add_context_from_file(file_path)

    def add_context(self, additional_context):
        self.prompt_retriever.add_context(additional_context)

    def overwrite_question(self, new_question):
        self.prompt_retriever.overwrite_question(new_question)

    def get_response(self):
        prompt = self.prompt_retriever.get_prompt()
        self.messages.append({"role": "user", "content": prompt})
        # Use the updated client method to create a chat completion
        response = self.client.chat.completions.create(
            messages=self.messages,
            model="gpt-4o"  # or your desired model
        )
      #   print(response)
      #   reply = response["choices"][0]["message"]["content"]
      #   self.messages.append({"role": "assistant", "content": reply})
        return response.choices[0].message.content



# Example usage
if __name__ == "__main__":
    question = "What is the current NDMI reading indicating for irrigation planning?"
    llm_interface = LLMInterface(question)

    file_path = "../eosdatacontext.txt"
    llm_interface.add_context_from_file(file_path)

    additional_context = "Additional context from satellite API."
    llm_interface.add_context(additional_context)

    response = llm_interface.get_response()
    print("Response from the chatbot:")
   #  print(response)
    reply = response.choices[0].message.content
    print(reply)
    ndvi_context = (
        "'NDVI': \n"
        "    'q1': 0.06225877162069082,\n"
        "    'q3': 0.15613897889852524,\n"
        "    'max': 0.2816303074359894,\n"
        "    'min': -0.11201691627502441,\n"
        "    'p10': 0.026399594917893413,\n"
        "    'p90': 0.18484574854373936,\n"
        "    'std': 0.06289542393441379,\n"
        "    'median': 0.10764970630407333,\n"
        "    'average': 0.1059820607514931,\n"
        "    'variance': 0.003955834351889631\n"
    )
   #  llm_interface.add_context(ndvi_context)
   #  response = llm_interface.get_response()
   #  print(response)
