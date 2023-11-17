#!/usr/bin/env python3

import sys

from bson.objectid import ObjectId

from .MongoConnection import MongoConnection

from ..model.Client import Client, ClientId


async def client_exists(client_id: int | str | ObjectId) -> bool:
    conn = MongoConnection("clientes")

    if isinstance(client_id, str):
        client_id = ObjectId(client_id)

    client = conn.collection.find_one({"_id": client_id})
    if client:
        return True

    return False


async def get_clients() -> list[ClientId]:
    conn = MongoConnection("clientes")
    clients = conn.collection.find()

    clients_list: list[ClientId] = []
    for client in clients:
        if client.get("id", None):
            client.pop("id")

        try:
            id = str(client.pop("_id"))
            client_obj = ClientId(id=id, **client)
            clients_list.append(client_obj)
        except TypeError:
            pass

    return clients_list


async def get_client_by_id(client_id: int | str | ObjectId) -> ClientId | None:
    conn = MongoConnection("clientes")
    if isinstance(client_id, str):
        client_id = ObjectId(client_id)

    client = conn.collection.find_one({"_id": client_id})

    if not client:
        return None

    id = str(client.pop("_id"))
    client_obj = ClientId(id=id, **client)
    return client_obj


async def create_client(client: Client) -> int:
    conn = MongoConnection("clientes")
    client_dict = client.model_dump()

    if client_dict.get("id", None):
        client_dict.pop("id")

    client_id = conn.collection.insert_one(client_dict).inserted_id

    return client_id


async def update_client_by_id(
    client_id: int | str | ObjectId, new_client: Client
) -> int | str | ObjectId | None:
    conn = MongoConnection("clientes")
    if isinstance(client_id, str):
        client_id = ObjectId(client_id)

    conn.collection.update_one({"_id": client_id}, {"$set": new_client.model_dump()})
    return client_id


async def delete_client(client_id: int | str | ObjectId) -> None:
    conn = MongoConnection("clientes")
    if isinstance(client_id, str):
        client_id = ObjectId(client_id)

    conn.collection.delete_one({"_id": client_id})

    return None


if __name__ == "__main__":
    print("This file is not supposed to be run manually.")
    print("Use run_api.sh or 'uvicorn main:app --reload' instead")
    sys.exit(1)
