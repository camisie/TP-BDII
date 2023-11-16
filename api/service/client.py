#!/usr/bin/env python3

import sys

from fastapi import HTTPException

from persistence.model.Client import Client
from persistence import client as clientDao


async def _client_return(
    rows: list[tuple[str, int], str, int] | tuple[str, int]
) -> dict:
    if not rows:
        return {}

    client_columns = [
        "id",
        "name",
        "surname",
        "address",
        "active",
        "code",
        "number",
        "kind",
    ]

    clients = {"clients": []}
    try:
        clients["clients"] = [dict(zip(client_columns, map(str, row))) for row in rows]

    except TypeError:
        clients["clients"] = [dict(zip(client_columns, map(str, rows)))]

    if len(clients["clients"]) == 1:
        return clients["clients"][0]

    return clients


async def get_clients() -> dict:
    client = await clientDao.get_clients()
    return await _client_return(client)


async def get_client_by_id(client_id: int) -> dict:
    client = await clientDao.get_client_by_id(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    return await _client_return(client)


async def create_client(client: Client) -> dict:
    new_id = await clientDao.create_client(client)

    return await get_client_by_id(new_id)


async def update_client_by_id(client_id: int, new_client: Client) -> dict:
    if not await clientDao.client_exists(client_id):
        raise HTTPException(status_code=404, detail="Client not found")

    await clientDao.update_client_by_id(client_id, new_client)
    return await get_client_by_id(client_id)


async def delete_client(client_id: int) -> dict:
    await clientDao.delete_client(client_id)
    return {}


if __name__ == "__main__":
    print("This file is not supposed to be run manually.")
    print("Use run_api.sh or 'uvicorn main:app --reload' instead")
    sys.exit(1)
