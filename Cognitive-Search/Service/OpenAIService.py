import openai
import os

# Definición constantes para el uso de Open AI.  Variable de entorno.
API_TYPE = os.environ["AZURE_OPENAI_API_TYPE"]
API_KEY = os.environ["AZURE_OPENAI_API_KEY"]
API_ENDPOINT = os.environ["AZURE_OPENAI_ENDPOINT"]
API_VERSION = os.environ["AZURE_OPENAI_VERSION"]

# Definición del modelo a usar para construir el Embedding (Vector) de la pregunta.
ENGINE_DAVINCI_UNIANDES = os.environ["MODEL_DAVINCI"]
ENGINE_ADA_UNIANDES = os.environ["MODEL_ADA"]

# Configuración y envío de parametros para conectarse al servicio de Azure Open AI.
openai.api_type = API_TYPE
openai.api_key = API_KEY
openai.api_base = API_ENDPOINT
openai.api_version = API_VERSION


def generate_completion_context(context, body_question):
    question = body_question["question"]
    response = openai.Completion.create(
        engine=ENGINE_DAVINCI_UNIANDES,
        prompt=f"""
        Eres un asistente virtual que ayuda a las personas a entender la constitución política de Colombia.
        Debes saludar a la persona, luego preguntarle si tiene alguna duda de la constitución política de Colombia.
        Debes identificar si la pregunta contiene lenguaje ofensivo, grosero o homofóbico.
        Solo estas capacitado a contestar preguntas de la constitución política de Colombia.
        De acuerdo unicamente al siguiente contexto:
        {context}.
        Responde la siguiente pregunta:
        {question}.
        Si la pregunta contiene lenguaje ofensivo, grosero o homofóbico, no respondas la pregunta y debes indicarle a la persona que solo se permiten preguntas relacionadas con la constitución política de Colombia.
        Si la pregunta no se puede responder usando el contexto, debe responder: “No tengo la información para responder esta pregunta”.
        La respuesta debe ser corta, muy amigable y conversacional
        """,
        max_tokens=150,
        temperature=0,
    )
    response_text = response.choices[0].text.strip()
    if "La pregunta no contiene lenguaje ofensivo, grosero o homofóbico." in response_text:
        response_text = response_text.replace("La pregunta no contiene lenguaje ofensivo, grosero o homofóbico.", "")
    return response_text
