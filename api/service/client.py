#!/usr/bin/env python3

import sys

from collections.abc import Awaitable

from fastapi import HTTPException
from pydantic import BaseModel


from .PsycopgCursor import PsycopgCursor


class Client(BaseModel):
    name: str
    surname: str
    address: str
    active: int


async def _client_return(fetch: Awaitable) -> dict:
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

    rows = await fetch()
    if not rows:
        return {}

    clients = {"clients": []}
    try:
        clients["clients"] = [dict(zip(client_columns, map(str, row))) for row in rows]

    except TypeError:
        clients["clients"] = [dict(zip(client_columns, map(str, rows)))]

    if len(clients["clients"]) == 1:
        return clients["clients"][0]

    return clients


async def _client_exists(client_id: int, aconn, acur) -> bool:
    await acur.execute(
        """
        SELECT
            1
        FROM e01_cliente AS client
        WHERE client.nro_cliente = (%s)
        """,
        (client_id,),
    )
    client = await acur.fetchone()
    if client:
        return True

    return False


async def client_exists(client_id: int) -> bool:
    async with PsycopgCursor() as (aconn, acur):
        return await _client_exists(client_id, aconn, acur)


async def get_clients() -> dict:
    async with PsycopgCursor() as (aconn, acur):
        await acur.execute(
            """
            SELECT
                nro_cliente, nombre, apellido, direccion, activo
            FROM e01_cliente
            """
        )

        return await _client_return(acur.fetchall)


async def get_client_by_id(client_id: int) -> dict:
    async with PsycopgCursor() as (aconn, acur):
        await acur.execute(
            """
             SELECT
                 nro_cliente, nombre, apellido, direccion, activo
             FROM e01_cliente
             WHERE nro_cliente = (%s)
             """,
            (client_id,),
        )

        client = await _client_return(acur.fetchone)
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")

        return client


async def create_client(client: Client) -> dict:
    async with PsycopgCursor() as (aconn, acur):
        await acur.execute(
            """
             INSERT INTO
                 e01_cliente (nombre, apellido, direccion, activo)
             VALUES
                 (%s, %s, %s, %s)
             RETURNING
                 nro_cliente
             """,
            (
                client.name,
                client.surname,
                client.address,
                client.active,
            ),
        )
        await aconn.commit()

        inserted_id = await acur.fetchone()
        inserted_id = inserted_id[0]

        return await get_client_by_id(inserted_id)


async def update_client_by_id(client_id: int, new_client: Client) -> dict:
    async with PsycopgCursor() as (aconn, acur):
        if not await _client_exists(client_id, aconn, acur):
            raise HTTPException(status_code=404, detail="Client not found")

        query = """
            UPDATE e01_cliente
            SET nombre = %(name)s, apellido = %(surname)s, 
                direccion = %(address)s,  activo = %(active)s
            WHERE nro_cliente = %(id)s
            """

        await aconn.execute(
            query,
            {
                "id": client_id,
                "name": new_client.name,
                "surname": new_client.surname,
                "address": new_client.address,
                "active": new_client.active,
            },
        )

        await aconn.commit()

        return await get_client_by_id(client_id)


async def delete_client(client_id: int) -> dict:
    async with PsycopgCursor() as (aconn, acur):
        await acur.execute(
            """
             DELETE 
             FROM e01_cliente 
             WHERE nro_cliente = (%s)
             """,
            (client_id,),
        )
        await aconn.commit()

        return {}


if __name__ == "__main__":
    print("This file is not supposed to be run manually.")
    print("Use run_api.sh or 'uvicorn main:app --reload' instead")
    sys.exit(1)
