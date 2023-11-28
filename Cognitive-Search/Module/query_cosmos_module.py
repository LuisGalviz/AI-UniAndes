import os

import Service.cosmos_service as cosmos_servcice

async def get_universities_bd():
    query = f'SELECT * FROM c'
    outings = await cosmos_servcice.read(f"{os.environ['CONTAINER_UNIVERSITIES']}", query)
    return outings

async def create_universities(body):
    try:
        if type(body) == list:
            for i in range(len(body)):
                await cosmos_servcice.create_update(f"{os.environ['CONTAINER_UNIVERSITIES']}", body[i])
        elif type(body) == dict:
            await cosmos_servcice.create_update(f"{os.environ['CONTAINER_UNIVERSITIES']}", body[i])
    except Exception as e:
        raise e