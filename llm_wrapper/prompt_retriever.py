class PromptRetrieverClass:
    def __init__(self, question):
        self.question = question
        self.context = ""
        self.prompt_template = (
            "You are an agricultural planning optimization assistant. Your role is to help farmers make data-driven "
            "decisions to optimize crop yields and resource usage. You have access to detailed farm data including NDMI "
            "measurements, soil moisture levels, weather forecasts, and more. When providing advice, integrate insights from "
            "this data to recommend the best planting schedules, irrigation strategies, and resource allocation. If any key "
            "details are unclear, ask for more information.\n\n"
            "Context:\n{context}\n\n"
            "Question: {question}\n"
            "Answer:"
        )

    def add_context_from_file(self, file_path):
        with open(file_path, 'r') as file:
            self.context += file.read() + "\n"

    def add_context(self, additional_context):
        self.context += additional_context + "\n"

    def overwrite_question(self, new_question):
        self.question = new_question

    def get_prompt(self):
        return self.prompt_template.format(context=self.context, question=self.question)