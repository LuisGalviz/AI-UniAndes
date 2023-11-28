import openai
import os

# Definición constantes para el uso de Open AI.  Variable de entorno.
API_TYPE = os.environ['AZURE_OPENAI_API_TYPE']
API_KEY = os.environ['CUSTOMCONNSTR_AZURE_OPENAI_API_KEY']
API_ENDPOINT = os.environ['CUSTOMCONNSTR_AZURE_OPENAI_ENDPOINT']
API_VERSION = os.environ['AZURE_OPENAI_VERSION']

# Definición del modelo a usar para construir el Embedding (Vector) de la pregunta.
ENGINE_DAVINCI_UNIANDES = os.environ['MODEL_DAVINCI']
ENGINE_ADA_UNIANDES = os.environ['MODEL_ADA']

#Configuración y envío de parametros para conectarse al servicio de Azure Open AI.
openai.api_type = API_TYPE
openai.api_key = API_KEY
openai.api_base = API_ENDPOINT
openai.api_version = API_VERSION



def generate_completion_context(context, body_question):
    question = body_question['question']
    response = openai.Completion.create(
        engine=ENGINE_DAVINCI_UNIANDES,
        prompt=f"""
        De acuerdo unicamente al siguiente contexto:
        {context}.
        Responde la siguiente pregunta:
        {question}
        """,
        max_tokens=150,
        temperature = 0
    )
    return response.choices[0].text