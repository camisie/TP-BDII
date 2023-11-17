#!/usr/bin/env python3

import sys
from os import environ

from fastapi import HTTPException

from persistence.model.Phone import Phone

if environ.get("API_DB", None) == "mongodb":
    from persistence.mongo import phone as phoneDao
    from persistence.mongo import client as clientDao

else:
    from persistence.postgresql import phone as phoneDao
    from persistence.postgresql import client as clientDao


async def _phone_return(rows: Phone | list[Phone]):
    phones = {"phones": []}
    if not rows:
        return phones

    if isinstance(rows, Phone):
        return rows.model_dump()

    phones["phones"] = rows
    return phones


async def get_phones() -> dict:
    phones = await phoneDao.get_phones()
    return await _phone_return(phones)


async def get_phone_by_client_id(client_id: int) -> dict:
    if not await clientDao.client_exists(client_id):
        raise HTTPException(status_code=404, detail="Client not found")

    phones = await phoneDao.get_phone_by_client_id(client_id)
    return await _phone_return(phones)


async def create_phone(client_id: int, phone: Phone) -> dict:
    if not await clientDao.client_exists(client_id):
        raise HTTPException(status_code=404, detail="Client not found")

    if await phoneDao.phone_exists(phone.codigo_area, phone.numero):
        raise HTTPException(status_code=409, detail="Phone already exists")

    await phoneDao.create_phone(client_id, phone)

    return await get_phone_by_client_id(client_id)


async def update_phone(client_id: int, phone: Phone) -> dict:
    if not await clientDao.client_exists(client_id):
        raise HTTPException(status_code=404, detail="Client not found")

    if not await phoneDao.phone_exists(phone.codigo_area, phone.numero):
        raise HTTPException(status_code=404, detail="Phone doesn't exist")

    await phoneDao.update_phone(client_id, phone)

    return await get_phone_by_client_id(client_id)


async def delete_phones(client_id: int):
    await phoneDao.delete_phones(client_id)

    return {}


async def delete_phone(client_id: int, code: int, number: int):
    if not await clientDao.client_exists(client_id):
        raise HTTPException(status_code=404, detail="Client not found")

    await phoneDao.delete_phone(client_id, code, number)

    return {}


if __name__ == "__main__":
    print("This file is not supposed to be run manually.")
    print("Use run_api.sh or 'uvicorn main:app --reload' instead")
    sys.exit(1)
