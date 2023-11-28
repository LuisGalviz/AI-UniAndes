import openai
import os

def generate_embeddings(text:str):

    openai.api_type = os.environ['AZURE_OPENAI_API_TYPE']
    openai.api_key = os.environ['CUSTOMCONNSTR_AZURE_OPENAI_API_KEY']
    openai.api_base = os.environ['CUSTOMCONNSTR_AZURE_OPENAI_ENDPOINT']
    openai.api_version = os.environ['AZURE_OPENAI_VERSION']
    
    model_ada = os.environ['MODEL_ADA']

    response = openai.Embedding.create(input=text,engine=model_ada)
    embeddings = response['data'][0]['embedding']
    return embeddings