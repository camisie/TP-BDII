#!/usr/bin/env python3

import sys

from bson.objectid import ObjectId
from .MongoConnection import MongoConnection

from ..model.Client import Client, ClientId
from ..model.Phone import Phone


def _get_connection():
    return MongoConnection("clientes")


def _get_id(
    id: int | str | ObjectId,
    connection: MongoConnection,
    alternative_id: str = "nro_cliente",
) -> ObjectId | None:
    return connection.get_id(id, alternative_id)


async def client_exists(client_id: int | str | ObjectId) -> bool:
    conn = _get_connection()
    id = _get_id(client_id, conn)
    if not id:
        return False

    client = conn.collection.find_one({"_id": id})
    if client:
        return True

    return False


def _model_phones(phones) -> list[Phone]:
    def _model_phone(phone) -> Phone:
        return Phone(**phone)

    phone_list: list[Phone] = []
    for phone in phones:
        phone_list.append(_model_phone(phone))

    return phone_list


async def get_clients() -> list[ClientId]:
    conn = _get_connection()
    clients = conn.collection.find()

    clients_list: list[ClientId] = []
    for client in clients:
        if client.get("id", None):
            client.pop("id")

        try:
            id = str(client.pop("_id"))
            phone = _model_phones(client.pop("telefono"))
            client_obj = ClientId(id=id, telefono=phone, **client)
            clients_list.append(client_obj)
        except TypeError:
            pass

    return clients_list


async def get_client_by_id(client_id: int | str | ObjectId) -> ClientId | None:
    conn = _get_connection()
    id = _get_id(client_id, conn)
    if not id:
        return None

    client = conn.collection.find_one({"_id": id})
    if not client:
        return None

    id = str(client.pop("_id"))
    phone = _model_phones(client.pop("telefono"))
    client_obj = ClientId(id=id, telefono=phone, **client)
    return client_obj


async def create_client(client: Client) -> int:
    conn = _get_connection()
    client_dict = client.model_dump()

    if client_dict.get("id", None):
        client_dict.pop("id")

    client_dict["nro_cliente"] = 0

    client_id = conn.collection.insert_one(client_dict).inserted_id

    return client_id


async def update_client_by_id(
    client_id: int | str | ObjectId, new_client: Client
) -> int | str | ObjectId | None:
    conn = _get_connection()
    id = _get_id(client_id, conn)
    if not id:
        return None

    client = conn.collection.find_one({"_id": id})

    new_client_obj = new_client.model_dump()
    new_client_obj["telefono"] = client.get("telefono", []) if client else []

    conn.collection.update_one({"_id": id}, {"$set": new_client_obj})

    return client_id


async def delete_client(client_id: int | str | ObjectId) -> None:
    conn = _get_connection()
    id = _get_id(client_id, conn)
    if not id:
        return None

    conn.collection.delete_one({"_id": id})

    return None


if __name__ == "__main__":
    print("This file is not supposed to be run manually.")
    print("Use run_api.sh or 'uvicorn main:app --reload' instead")
    sys.exit(1)
