import azure.functions as func
import logging
import json
import os
import Services.langchain_services as langchain_services

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.function_name(name="PostLangChainConsultRetriver")
@app.route(route="langchain/retriever/consult", auth_level=func.AuthLevel.ANONYMOUS, methods=['POST'])
def generate_embeddings_json(req: func.HttpRequest) -> func.HttpResponse:
    try:
        request_body = req.get_json() 
        response = langchain_services.retriever_as_vector_store(request_body["question"])
        return func.HttpResponse(json.dumps({"answer": response}), headers={"content-type": "application/json"})
    except Exception as e:
        logging.error(e)
        return func.HttpResponse(e)


@app.function_name(name="UpdateFileLangChain")
@app.blob_trigger(arg_name="myblob", path="universidad/{name}", connection="STORAGE_CONECTION")
def upload_file(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob \n"
            f"Name: {myblob.name} \n"
            f"Blob Size: {myblob.length} byte \n")
    langchain_services.process_load_data_lang_chain(str(myblob.name).replace("universidad/", ""))