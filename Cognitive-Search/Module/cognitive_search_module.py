import Service.cognitive_search_service as client_cognitive
import Util.embedding as embd
import os

index = os.environ['INDEX']

def search_cognitive_search(body):
    question = body['question']

    vector_question = embd.generate_embeddings(question)

    client_cognitive_search = client_cognitive.create_cognitive_search_client(index)
    
    cognitive_search = client_cognitive_search.search(top= 5, search_text=f"{question}")

    context = ""
    for result in cognitive_search:
        if result["@search.score"] >= 0.4:
            context_ini = "Id: {}. \nContenido: {}.)".format(result["id"], result["content"])
            context += context_ini + "\n"
    return context