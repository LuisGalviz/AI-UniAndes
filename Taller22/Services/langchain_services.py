
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import AzureBlobStorageContainerLoader
from langchain.docstore.document import Document
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.azuresearch import AzureSearch
from typing import List

embeddings = OpenAIEmbeddings(deployment=os.environ['ENGINE_ADA_UNIANDES'])

def document_loader_pdf(name_file:str) -> List[Document]:
  loader = AzureBlobStorageContainerLoader(conn_str=os.environ['CUSTOMCONNSTR_STORAGE_CONECTION'], container="universidad", prefix=name_file)
  return loader.load()

def text_splitter_by_caracter(documents:List[Document]) -> List[Document]:
  chunk_size = 500
  chunk_overlap = 30
  text_splitter = RecursiveCharacterTextSplitter(
      chunk_size=chunk_size, chunk_overlap=chunk_overlap, 
  )

  splits = text_splitter.split_documents(documents)
  print("Cantidad Documentos --> ", len(splits))
  return splits


def vector_store_azure_search(documents:List[Document]) -> None:
  index_name: str = "universidades-langchain-vector"

  vector_store: AzureSearch = AzureSearch(
      azure_search_endpoint= os.environ['COGNITIVE_SEARCH_ENDPOINT'],
      azure_search_key = os.environ['CUSTOMCONNSTR_COGNITIVE_SEARCH_API_KEY'],
      index_name=index_name,
      embedding_function=embeddings.embed_query,
  )
  #cargar documentos
  vector_store.add_documents(documents=documents)


def retriever_as_vector_store(query:str) -> List[str]:
  index_name: str = "universidades-langchain-vector"

  vector_store: AzureSearch = AzureSearch(
      azure_search_endpoint= os.environ['COGNITIVE_SEARCH_ENDPOINT'],
      azure_search_key = os.environ['CUSTOMCONNSTR_COGNITIVE_SEARCH_API_KEY'],
      index_name=index_name,
      embedding_function=embeddings.embed_query,
  )

  #También puede establecer un método de recuperación que establezca un umbral de puntuación de similitud y solo devuelva documentos con una puntuación superior a ese umbral.
  retriever = vector_store.as_retriever(search_type="similarity_score_threshold", search_kwargs={"score_threshold": .5})
  docs:List[Document] = retriever.get_relevant_documents(query)
  page_contents:List[str] = [doc.page_content for doc in docs]
  return page_contents

def process_load_data_lang_chain(name_file:str) -> None:
  print("\n .... Comenzo proceso de cargue .... ")
  print("\n .... Lectura de archivo .... ")
  list_document:List[Document] = document_loader_pdf(name_file) 
  print("\n .... Split de documentos .... ")
  documents_splitter:List[Document] = text_splitter_by_caracter(list_document)
  print("\n .... Cargue al vector storage .... ")
  vector_store_azure_search(documents_splitter) 
  print("\n .... Finalizo proceso de cargue .... ")
  