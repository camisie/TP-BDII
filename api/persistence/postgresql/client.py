#!/usr/bin/env python3

import sys

from .PsycopgCursor import PsycopgCursor

from ..model.Client import Client, ClientId


def _map_to_clientid(row) -> ClientId | None:
    if not row:
        return None

    client_columns = list(ClientId.__annotations__.keys())

    client = dict(zip(client_columns, row))
    client["id"] = str(client.get("id", ""))
    return ClientId(**client)


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


async def get_clients() -> list[ClientId] | None:
    async with PsycopgCursor() as (aconn, acur):
        await acur.execute(
            """
             SELECT
                 nro_cliente, nombre, apellido, direccion, activo
             FROM e01_cliente
             """
        )

        clients = await acur.fetchall()
        if not clients:
            return None

        mapped = [_map_to_clientid(client) for client in clients]
        return [client for client in mapped if client is not None]


async def get_client_by_id(
    client_id: int | str,
) -> ClientId | None:
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

        result = await acur.fetchone()
        if not result:
            return None

        client = _map_to_clientid(result)
        return client


async def create_client(client: Client) -> int:
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
                client.nombre,
                client.apellido,
                client.direccion,
                client.activo,
            ),
        )
        await aconn.commit()

        inserted_id = await acur.fetchone()
        return inserted_id[0]


async def update_client_by_id(client_id: int, new_client: Client) -> int:
    async with PsycopgCursor() as (aconn, acur):
        await aconn.execute(
            """
            UPDATE e01_cliente
            SET nombre = %(name)s, apellido = %(surname)s, 
                direccion = %(address)s,  activo = %(active)s
            WHERE nro_cliente = %(id)s
            """,
            {
                "id": client_id,
                "name": new_client.nombre,
                "surname": new_client.apellido,
                "address": new_client.direccion,
                "active": new_client.activo,
            },
        )

        await aconn.commit()

        return client_id


async def delete_client(client_id: int) -> None:
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


if __name__ == "__main__":
    print("This file is not supposed to be run manually.")
    print("Use run_api.sh or 'uvicorn main:app --reload' instead")
    sys.exit(1)
