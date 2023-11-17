#!/usr/bin/env python3

import sys

from typing import Any

from fastapi import HTTPException

from persistence.model.Client import Client, ClientId

# from persistence.postgresql import client as clientDao
from persistence.mongo import client as clientDao


async def _client_return(rows: list[ClientId] | ClientId) -> dict:
    if not rows:
        return {}

    clients = {"clients": []}

    if isinstance(rows, ClientId):
        return rows.model_dump()

    if isinstance(rows[0], ClientId):
        clients["clients"] = rows
        return clients

    return {}


async def get_clients():
    clients = await clientDao.get_clients()
    return await _client_return(clients)


async def get_client_by_id(client_id: int | str):
    client = await clientDao.get_client_by_id(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    return await _client_return(client)


async def create_client(client: Client) -> ClientId:
    new_id = await clientDao.create_client(client)

    return await get_client_by_id(new_id)


async def update_client_by_id(client_id: int | str, new_client: Client) -> ClientId:
    if not await clientDao.client_exists(client_id):
        raise HTTPException(status_code=404, detail="Client not found")

    id = await clientDao.update_client_by_id(client_id, new_client)
    if not id:
        raise HTTPException(status_code=404, detail="Client not found")

    return await get_client_by_id(client_id)


async def delete_client(client_id: int | str) -> dict[None:None]:
    await clientDao.delete_client(client_id)
    return {}


if __name__ == "__main__":
    print("This file is not supposed to be run manually.")
    print("Use run_api.sh or 'uvicorn main:app --reload' instead")
    sys.exit(1)
