#!/usr/bin/env python3

import sys

from collections.abc import Awaitable

from fastapi import HTTPException
from pydantic import BaseModel


from .PsycopgCursor import PsycopgCursor

import service.client as client_service
from .client import Client


class Phone(BaseModel):
    code: int
    number: int
    kind: str


async def _phone_return(fetch: Awaitable) -> dict:
    phone_columns = ["code", "number", "kind", "client_id"]
    phones = {"phones": []}

    rows = await fetch()
    if not rows:
        return phones

    try:
        phones["phones"] = [dict(zip(phone_columns, map(str, row))) for row in rows]

    except TypeError:
        phones["phones"] = [dict(zip(phone_columns, map(str, rows)))]

    return phones


async def _phone_exists(code: int, number: int, aconn, acur) -> bool:
    await acur.execute(
        """
        SELECT
            1
        FROM e01_telefono
        WHERE codigo_area = (%s) AND nro_telefono = (%s)
        """,
        (
            code,
            number,
        ),
    )

    phone = await acur.fetchone()
    if phone:
        return True

    return False


async def phone_exists(code: int, number: int) -> bool:
    async with PsycopgCursor() as (aconn, acur):
        return await _phone_exists(code, number, aconn, acur)


async def get_phones() -> dict:
    async with PsycopgCursor() as (aconn, acur):
        await acur.execute(
            """
            SELECT
                codigo_area, nro_telefono, tipo, nro_cliente
            FROM e01_telefono
            """
        )

        return await _phone_return(acur.fetchall)


async def get_phone_by_client_id(client_id: int) -> dict:
    if not await client_service.client_exists(client_id):
        raise HTTPException(status_code=404, detail="Client not found")

    async with PsycopgCursor() as (aconn, acur):
        await acur.execute(
            """
             SELECT
                 codigo_area, nro_telefono, tipo, nro_cliente
             FROM e01_telefono 
             WHERE nro_cliente = (%s)
             """,
            (client_id,),
        )

        return await _phone_return(acur.fetchall)


async def _create_phone(client_id: int, phone: Phone) -> dict:
    async with PsycopgCursor() as (aconn, acur):
        await acur.execute(
            """
              INSERT INTO
                  e01_telefono (codigo_area, nro_telefono, tipo, nro_cliente)
              VALUES
                  (%s, %s, %s, %s)
              """,
            (phone.code, phone.number, phone.kind, client_id),
        )
        await aconn.commit()

        return await get_phone_by_client_id(client_id)


async def _update_phone(client_id: int, new_phone: Phone) -> dict:
    async with PsycopgCursor() as (aconn, acur):
        query = """
            UPDATE e01_telefono
            SET tipo = %(kind)s, nro_cliente = %(id)s
            WHERE codigo_area = %(code)s AND nro_telefono = %(number)s 
            """

        await aconn.execute(
            query,
            {
                "kind": new_phone.kind,
                "id": client_id,
                "code": new_phone.code,
                "number": new_phone.number,
            },
        )

        await aconn.commit()


async def create_phone(client_id: int, phone: Phone) -> dict:
    if not await client_service.client_exists(client_id):
        raise HTTPException(status_code=404, detail="Client not found")

    if await phone_exists(phone.code, phone.number):
        raise HTTPException(status_code=409, detail="Phone already exists")

    return await _create_phone(client_id, phone)


async def update_phone(client_id: int, phone: Phone) -> dict:
    if not await client_service.client_exists(client_id):
        raise HTTPException(status_code=404, detail="Client not found")

    if not await phone_exists(phone.code, phone.number):
        raise HTTPException(status_code=404, detail="Phone doesn't exist")

    await _update_phone(client_id, phone)

    return await get_phone_by_client_id(client_id)


async def delete_phones(client_id: int):
    async with PsycopgCursor() as (aconn, acur):
        await acur.execute(
            """
             DELETE 
             FROM e01_telefono
             WHERE nro_cliente = (%s)
             """,
            (client_id,),
        )
        await aconn.commit()

        return {}


async def delete_phone(client_id: int, code: int, number: int):
    async with PsycopgCursor() as (aconn, acur):
        await acur.execute(
            """
             DELETE 
             FROM e01_telefono
             WHERE nro_cliente = (%s) AND codigo_area = (%s) AND nro_telefono = (%s)
             """,
            (client_id, code, number),
        )
        await aconn.commit()

        return {}


if __name__ == "__main__":
    print("This file is not supposed to be run manually.")
    print("Use run_api.sh or 'uvicorn main:app --reload' instead")
    sys.exit(1)
