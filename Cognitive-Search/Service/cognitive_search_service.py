import azure.functions as func
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
import os

search_api_key  = os.environ['COG_SEAR_API_KEY']
search_endpoint = os.environ['COG_SEAR_ENDPOINT']

search_credential = AzureKeyCredential(search_api_key)

def create_cognitive_search_client(cognitive_search_index):
    cognitive_search_client = SearchClient(
        endpoint=search_endpoint, 
        index_name=cognitive_search_index, 
        credential=search_credential
        )
    return cognitive_search_client