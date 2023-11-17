#!/usr/bin/env python3

import sys

from bson.objectid import ObjectId
from .MongoConnection import MongoConnection

from .client import get_client_by_id
from ..model.Phone import Phone


def _get_client_id(
    id: int | str | ObjectId,
    connection: MongoConnection,
    alternative_id: str = "nro_cliente",
) -> ObjectId | None:
    return connection.get_id(id, alternative_id)


def _get_connection():
    return MongoConnection("clientes")


async def phone_exists(code: int, number: int) -> bool:
    conn = _get_connection()
    result = conn.collection.find_one(
        {"telefono": {"$elemMatch": {"codigo_area": code, "numero": number}}},
        {"telefono.$": 1},
    )

    if result:
        return True

    return False

    phone = await acur.fetchone()
    if phone:
        return True

    return False


def _get_phone_from_query(phone) -> list[Phone]:
    phones_list: list[Phone] = []
    if (
        "telefono" in phone
        and isinstance(phone["telefono"], list)
        and len(phone["telefono"]) > 0
    ):
        for p in phone["telefono"]:
            phones_list.append(Phone(**p))

    return phones_list


async def get_phones() -> list[Phone]:
    conn = _get_connection()
    phones = conn.collection.find({}, {"telefono": 1})

    phones_list: list[Phone] = []

    for phone in phones:
        phones_obj = _get_phone_from_query(phone)

        for p in phones_obj:
            phones_list.append(p)

    return phones_list


async def get_phone_by_client_id(client_id: int | str | ObjectId) -> list[Phone]:
    conn = _get_connection()
    id = _get_client_id(client_id, conn)
    phone = conn.collection.find_one({"_id": id}, {"telefono": 1})

    return _get_phone_from_query(phone)


async def create_phone(
    client_id: int | str | ObjectId, phone: Phone
) -> ObjectId | None:
    conn = _get_connection()
    id = _get_client_id(client_id, conn)

    conn.collection.update_one({"_id": id}, {"$push": {"telefono": phone.model_dump()}})

    return id


async def update_phone(client_id: int, new_phone: Phone) -> ObjectId | None:
    conn = _get_connection()
    id = _get_client_id(client_id, conn)

    conn.collection.update_one(
        {
            "_id": id,
            "telefono": {
                "$elemMatch": {
                    "codigo_area": new_phone.codigo_area,
                    "numero": new_phone.numero,
                }
            },
        },
        {"$set": {"telefono.$": new_phone.model_dump()}},
    )

    return id


async def delete_phones(client_id: int) -> None:
    conn = _get_connection()
    id = _get_client_id(client_id, conn)

    conn.collection.update_one({"_id": id}, {"$set": {"telefono": []}})


async def delete_phone(client_id: int, code: int, number: int) -> None:
    conn = _get_connection()
    id = _get_client_id(client_id, conn)

    conn.collection.update_one(
        {"_id": id},
        {
            "$pull": {"telefono": {"codigo_area": code, "numero": number}},
        },
    )

    return None


if __name__ == "__main__":
    print("This file is not supposed to be run manually.")
    print("Use run_api.sh or 'uvicorn main:app --reload' instead")
    sys.exit(1)
