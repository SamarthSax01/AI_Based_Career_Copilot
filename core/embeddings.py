from langchain_mistralai import MistralAIEmbeddings
import os
from dotenv import load_dotenv
load_dotenv()
def get_embedding_model():
    embedding_model=MistralAIEmbeddings(
        model="mistral-embed",
        api_key=os.getenv("MISTRAL_API_KEY")
    )
    return embedding_model
          