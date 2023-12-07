from azure.cosmos.aio import CosmosClient as cosmos_client
from azure.cosmos import PartitionKey, exceptions
import logging
import os

endpoint = f"{os.environ['COSMOSDB_ENDPOINT']}"
key = f"{os.environ['COSMOSDB_KEY']}"
database_name = f"{os.environ['DATABASE_NAME']}"


async def get_db(client, database_name):
    try:
        database_obj = client.get_database_client(database_name)
        await database_obj.read()
        return database_obj
    except exceptions.CosmosResourceNotFoundError:
        print("Base de datos no existe.")
        raise Exception("Base de datos no existe.")


async def get_container(database_obj, container_name):
    try:
        todo_items_container = database_obj.get_container_client(container_name)
        await todo_items_container.read()
        return todo_items_container
    except exceptions.CosmosResourceNotFoundError as e:
        print("Container no existe.")
        raise Exception("Container no existe.")
    except exceptions.CosmosHttpResponseError as e:
        raise e


async def read_items(container_obj, items_to_read):
    for family in items_to_read:
        item_answer = await container_obj.read_item(
            item=family["id"], partition_key=family["lastName"]
        )
        request_charge = container_obj.client_connection.last_answer_headers[
            "x-ms-request-charge"
        ]
        print(
            "Read item with id {0}. Operation consumed {1} request units".format(
                item_answer["id"], (request_charge)
            )
        )


async def query_items(container_obj, query_text):
    query_items_answer = container_obj.query_items(query=query_text)
    request_charge = container_obj.client_connection.last_response_headers[
        "x-ms-request-charge"
    ]
    items = [item async for item in query_items_answer]
    print(
        "Query returned {0} items. Operation consumed {1} request units".format(
            len(items), request_charge
        )
    )
    return items


async def read(container_name, query):
    async with cosmos_client(endpoint, credential=key) as client:
        try:
            database_obj = await get_db(client, database_name)
            container_obj = await get_container(database_obj, container_name)
            var_await = await query_items(container_obj, query)
            return var_await
        except exceptions.CosmosHttpResponseError as e:
            logging.error(e.message)
            raise Exception(
                f"Ocurrio un error al momento de buscar en {container_name}"
            )


async def create_update(container_name, body):
    async with cosmos_client(endpoint, credential=key) as client:
        try:
            database_obj = await get_db(client, database_name)
            container_obj = await get_container(database_obj, container_name)
            await container_obj.upsert_item(body)
        except exceptions.CosmosHttpResponseError as e:
            logging.error(e.message)
            raise Exception(
                f"Ocurrio un error al momento de actualizar en {container_name}"
            )


async def delete(container_name, doc_id, partition_key):
    async with cosmos_client(endpoint, credential=key) as client:
        try:
            database_obj = await get_db(client, database_name)
            container_obj = await get_container(database_obj, container_name)
            await container_obj.delete_item(doc_id, partition_key)
        except exceptions.CosmosHttpResponseError as e:
            logging.error(e.message)
            raise Exception(
                f"Ocurrio un error al momento de eliminar en {container_name}"
            )
