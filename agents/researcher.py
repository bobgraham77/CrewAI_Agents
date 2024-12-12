import os
from dotenv import load_dotenv
from transformers import AutoModelForCausalLM, AutoTokenizer
import openai

# Load environment variables
load_dotenv()

class ResearcherAgent:
    def __init__(self, openai=True):
        if openai:
            self.api_key = os.environ.get('OPENAI_API_KEY')  # Keep this for compatibility
            if not self.api_key:
                raise ValueError("OPENAI_API_KEY not found in environment variables")
            openai.api_key = self.api_key
        else:
            self.tokenizer = AutoTokenizer.from_pretrained('meta-llama/Llama-3-3')
            self.model = AutoModelForCausalLM.from_pretrained('meta-llama/Llama-3-3')

    def search_web(self, topic):
        # Placeholder for web search logic
        return f"Results for {topic} from web search."

    def search_youtube(self, topic):
        # Placeholder for YouTube search logic
        return f"Results for {topic} from YouTube search."

    def compile_results(self, web_results, youtube_results):
        # Combine results into a single document
        return f"Compiled document with web and YouTube results for {web_results} and {youtube_results}."

    def summarize_key_points(self, compiled_document):
        if hasattr(self, 'model'):
            inputs = self.tokenizer(compiled_document, return_tensors='pt')
            outputs = self.model.generate(**inputs)
            return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        else:
            # OpenAI summarization logic
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"Summarize the following document: {compiled_document}",
                max_tokens=150
            )
            return response.choices[0].text.strip()

    def perform_research(self, topic):
        try:
            web_results = self.search_web(topic)
            youtube_results = self.search_youtube(topic)
            compiled_document = self.compile_results(web_results, youtube_results)
            summary = self.summarize_key_points(compiled_document)
            return summary
        except Exception as e:
            return f"Error performing research: {str(e)}"
