#!/usr/bin/env python3

import sys

from .PsycopgCursor import PsycopgCursor

from .model.Client import Client


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


async def get_clients() -> list[tuple[str, int], str, int] | tuple[str, int]:
    async with PsycopgCursor() as (aconn, acur):
        await acur.execute(
            """
             SELECT
                 nro_cliente, nombre, apellido, direccion, activo
             FROM e01_cliente
             """
        )

        return await acur.fetchall()


async def get_client_by_id(
    client_id: int,
) -> list[tuple[str, int], str, int] | tuple[str, int]:
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

        return await acur.fetchone()


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
                client.name,
                client.surname,
                client.address,
                client.active,
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
                "name": new_client.name,
                "surname": new_client.surname,
                "address": new_client.address,
                "active": new_client.active,
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
