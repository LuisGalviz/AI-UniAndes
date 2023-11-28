import os
from langchain.chat_models import AzureChatOpenAI
from langchain.llms import AzureOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.prompts import HumanMessagePromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain.output_parsers import XMLOutputParser
from langchain.output_parsers import JsonOutputToolsParser
from langchain.schema import AIMessage

from langchain.chains import ConversationChain
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.memory import RedisChatMessageHistory
from langchain.output_parsers import RetryWithErrorOutputParser

from Model.movie import Movie
from typing import Union

chat_model: AzureChatOpenAI = AzureChatOpenAI(temperature=0, deployment_name=os.environ['MODEL_BASE_GPT_TURBO'])
llm = AzureOpenAI(temperature=0, deployment_name=os.environ["MODEL_BASE_DAVINCI"])




def prompt_template(parser: Union[XMLOutputParser, PydanticOutputParser]) -> ChatPromptTemplate:
    template_string = """responder a la pregunta de los usuarios lo mejor posible
    solo vas a responder preguntas relacionadas con el tema del cine
    responder con la estructura descrita en el formato_instrucciones
    pregunta:
    {question}
    formato_instrucciones:
    {format_instructions}"""

    return ChatPromptTemplate(
        messages=[
            HumanMessagePromptTemplate.from_template(template_string)
        ],
        input_variables=["question"],
        partial_variables={"format_instructions": parser.get_format_instructions()})

# def prompt_template_memory() -> ChatPromptTemplate:
#     template_string = """responder a las preguntas de los usuarios lo mejor posible
#     Interactuar de manera amigable y cordial
#     pregunta:
#     {question}"""

#     return ChatPromptTemplate(
#         messages=[
#             HumanMessagePromptTemplate.from_template(template_string)
#         ],
#         input_variables=["question"])


def output_string_json() -> PydanticOutputParser:
    return PydanticOutputParser(pydantic_object=Movie)


def output_string_xml() -> XMLOutputParser:
    return XMLOutputParser(tags=["movies", "actor", "film", "name", "genre"])


def execute_chain(query: str, type_output:str) -> str:
    parser: Union[XMLOutputParser, PydanticOutputParser] = output_string_xml() if type_output == "XML" else output_string_json()
    prompt: ChatPromptTemplate = prompt_template(parser)
    chain = prompt | chat_model
    output:AIMessage = chain.invoke({"question": query})

    return output.content

def execute_chain_memory(query: str, id: str) -> str:
    #prompt: ChatPromptTemplate = prompt_template_memory()
    message_history: RedisChatMessageHistory = conversation_redis_memory(id)
    memory: ConversationBufferMemory = ConversationBufferMemory(chat_memory=message_history)
    #chain = LLMChain(llm=chat_model,  prompt=prompt,  memory=memory)
    conversation = ConversationChain(llm=llm, memory=memory)
    output = conversation.predict(input= query)
    print("Memoria --> ", memory.buffer)
    return output

def conversation_redis_memory(id: str) -> RedisChatMessageHistory:
    """
    Es la mezcla para guardar todo el historial de memoria en un servicio externo en redis
    """

    return RedisChatMessageHistory(
      session_id= id,
      key_prefix = os.environ["KEY_PREFIX_REDIS"],
      url = os.environ["URL_REDIS"],
      ttl = os.environ["TTL_REDIS"]
    )

def reset__memory() -> None:
    #prompt: ChatPromptTemplate = prompt_template_memory()
    message_history: RedisChatMessageHistory = conversation_redis_memory()
    message_history.clear()