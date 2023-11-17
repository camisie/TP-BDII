#!/usr/bin/env python3

import sys

from .PsycopgCursor import PsycopgCursor

from .model.Phone import Phone


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


async def get_phones() -> list[tuple[str, int], str, int] | tuple[str, int]:
    async with PsycopgCursor() as (aconn, acur):
        await acur.execute(
            """
            SELECT
                codigo_area, nro_telefono, tipo, nro_cliente
            FROM e01_telefono
            """
        )

        return await acur.fetchall()


async def get_phone_by_client_id(
    client_id: int,
) -> list[tuple[str, int], str, int] | tuple[str, int]:
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

        return await acur.fetchall()


async def create_phone(client_id: int, phone: Phone) -> int:
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

        return client_id


async def update_phone(client_id: int, new_phone: Phone) -> int:
    async with PsycopgCursor() as (aconn, acur):
        await aconn.execute(
            """
            UPDATE e01_telefono
            SET tipo = %(kind)s, nro_cliente = %(id)s
            WHERE codigo_area = %(code)s AND nro_telefono = %(number)s 
            """,
            {
                "kind": new_phone.kind,
                "id": client_id,
                "code": new_phone.code,
                "number": new_phone.number,
            },
        )

        await aconn.commit()
        return client_id


async def delete_phones(client_id: int) -> None:
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


async def delete_phone(client_id: int, code: int, number: int) -> None:
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


if __name__ == "__main__":
    print("This file is not supposed to be run manually.")
    print("Use run_api.sh or 'uvicorn main:app --reload' instead")
    sys.exit(1)
