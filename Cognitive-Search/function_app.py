import azure.functions as func
import logging
import json
import Service.OpenAIService as OpenAIService
import Module.query_cosmos_module as query_cosmos
import Module.cognitive_search_module as cog_search

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.function_name(name="GetUniversities")
@app.route(route="get/universities", auth_level=func.AuthLevel.ANONYMOUS, methods=['GET'])
async def get_universities(req: func.HttpRequest) -> func.HttpResponse:
    try:
        all_universities = await query_cosmos.get_universities_bd()
        return func.HttpResponse(json.dumps(all_universities), headers={"content-type": "application/json"})
    except Exception as e:
        logging.error(e)
        return func.HttpResponse(e)
    
@app.function_name(name="PostUniversities")
@app.route(route="post/universities", auth_level=func.AuthLevel.ANONYMOUS, methods=['POST'])
async def post_universities(req: func.HttpRequest) -> func.HttpResponse:
    request_body = req.get_json()
    try:
        await query_cosmos.create_universities(request_body)

        return func.HttpResponse(json.dumps({"response": "The object has been successfully created."}), headers={"content-type": "application/json"})
    except Exception as e:
        logging.error(e)
        return func.HttpResponse(e)

@app.function_name(name="GetContext")
@app.route(route="get/context", auth_level=func.AuthLevel.ANONYMOUS, methods=['POST'])
async def get_context(req: func.HttpRequest) -> func.HttpResponse:
    try:
        request_body = req.get_json()      
        context = cog_search.search_cognitive_search(request_body)
        return func.HttpResponse(json.dumps({"contexto": context}), headers={"content-type": "application/json"})
    except Exception as e:
        logging.error(e)
        return func.HttpResponse(e)
    

@app.function_name(name="GetContextPostQuestion")
@app.route(route="chat/completion/cognitive", auth_level=func.AuthLevel.ANONYMOUS, methods=['POST'])
async def chat_completion_with_context(req: func.HttpRequest) -> func.HttpResponse:
    try:
        request_body = req.get_json()      
        context = cog_search.search_cognitive_search(request_body)
        result = OpenAIService.generate_completion_context(context, request_body)
        return func.HttpResponse(json.dumps({"answer": result}), headers={"content-type": "application/json"})
    except Exception as e:
        logging.error(e)
        return func.HttpResponse(e)