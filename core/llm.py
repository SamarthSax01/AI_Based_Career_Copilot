from langchain_mistralai import ChatMistralAI
from dotenv import load_dotenv
load_dotenv()
import os
def get_llm():
    llm=ChatMistralAI(
        model="mistral-small-latest",
        api_key=os.getenv("MISTRAL_API_KEY"),
        temperature=0.2
    )
    return llm