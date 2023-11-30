import azure.functions as func
import Service.langChainService as langchain_service
import logging
import json
import uuid

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.function_name(name="PostLangChainParserOutPut")
@app.route(route="langchain/output", auth_level=func.AuthLevel.ANONYMOUS, methods=['POST'])
def conversation_langchain(req: func.HttpRequest) -> func.HttpResponse:
    try:
        request_body = req.get_json() 
        response = langchain_service.execute_chain(request_body["question"], request_body["typeOut"]) 
        data = response if request_body["typeOut"] == "XML" else json.dumps(json.loads(response))
        content_type = "text/xml" if request_body["typeOut"] == "XML" else "application/json"
        return func.HttpResponse(data, headers={"content-type": content_type })
    except Exception as e:
        logging.error(e)
        return func.HttpResponse(e)

@app.function_name(name="PostLangChainConversation")
@app.route(route="langchain/chat", auth_level=func.AuthLevel.ANONYMOUS, methods=['POST'])
def conversation_langchain(req: func.HttpRequest) -> func.HttpResponse:
    try:
        request_body = req.get_json()
        id = request_body['id']
        if id == "":
            id = str(uuid.uuid4())
        response = langchain_service.execute_chain_memory(request_body["question"], id)
        return func.HttpResponse(json.dumps({"id": id, "answer": response}), headers={"content-type": "application/json"})
    except Exception as e:
        logging.error(e)
        return func.HttpResponse(e)

@app.function_name(name="GetResetHistoryChat")
@app.route(route="langchain/reset", auth_level=func.AuthLevel.ANONYMOUS, methods=['GET'])
def conversation_langchain(req: func.HttpRequest) -> func.HttpResponse:
    try:
        langchain_service.reset__memory()
        return func.HttpResponse(json.dumps({"message": "Se ha reseteado el historial del chat"}), headers={"content-type": "application/json"})
    except Exception as e:
        logging.error(e)
        return func.HttpResponse(e)
    
    