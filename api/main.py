#!/usr/bin/env python3

import sys

from collections.abc import Awaitable

from fastapi import FastAPI
from pydantic import BaseModel

import psycopg

app = FastAPI()


class PsycopgCursor:
    def __init__(self):
        pass

    async def __aenter__(self):
        self.aconn = await psycopg.AsyncConnection.connect("dbname=bd2-tpo")
        self.cursor = self.aconn.cursor()
        return (self.aconn, self.cursor)

    async def __aexit__(self, exception_type, exception_value, exception_traceback):
        await self.aconn.commit()
        await self.cursor.close()
        await self.aconn.close()


class Phone(BaseModel):
    code: int
    number: int
    kind: str


class Client(BaseModel):
    name: str
    surname: str
    address: str
    active: int
    phone: Phone | list[Phone]


async def client_return(fetch: Awaitable) -> dict | list[dict]:
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
    phone_columns = ["code", "number", "kind"]

    rows = await fetch()
    if not rows:
        return {}

    clients = {}
    try:
        clients["clients"] = [dict(zip(client_columns, map(str, row))) for row in rows]

    except TypeError:
        clients["clients"] = [dict(zip(client_columns, map(str, rows)))]

    for client in clients["clients"]:
        phone_data = {key: str(client.pop(key, None)) for key in phone_columns}
        client["phone"] = phone_data

    if len(clients["clients"]) == 1:
        clients["clients"] = clients["clients"][0]

    return clients


@app.get("/clients")
async def get_clients():
    async with PsycopgCursor() as (aconn, acur):
        await acur.execute(
            """
            SELECT 
                client.nro_cliente, nombre, apellido, direccion, activo,
                codigo_area, nro_telefono, tipo
            FROM e01_cliente AS client 
            LEFT JOIN e01_telefono AS phone
                ON client.nro_cliente = phone.nro_cliente
            """
        )

        return await client_return(acur.fetchall)


@app.get("/clients/{client_id}")
async def get_client(client_id: int):
    async with PsycopgCursor() as (aconn, acur):
        await acur.execute(
            """
            SELECT
                client.nro_cliente, nombre, apellido, direccion, activo,
                codigo_area, nro_telefono, tipo
            FROM e01_cliente AS client 
            LEFT JOIN e01_telefono AS phone
                ON client.nro_cliente = phone.nro_cliente
            WHERE client.nro_cliente = (%s)
            """,
            (client_id,),
        )

        return await client_return(acur.fetchone)


@app.post("/clients")
async def create_client(client: Client):
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

        await acur.execute(
            """
            INSERT INTO 
                e01_telefono (codigo_area, nro_telefono, tipo, nro_cliente)
            VALUES
                (%s, %s, %s, %s)
            """,
            (client.phone.code, client.phone.number, client.phone.kind, inserted_id[0]),
        )
        await aconn.commit()

        return await get_client(inserted_id[0])


if __name__ == "__main__":
    print("This file is not supposed to be run manually.")
    print("Use run_api.sh or 'uvicorn main:app --reload' instead")
    sys.exit(1)
