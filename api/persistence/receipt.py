#!/usr/bin/env python3

import sys


from .PsycopgCursor import PsycopgCursor


async def _receipt_exists(receipt_id: int, aconn, acur) -> bool:
    await acur.execute(
        """
        SELECT
            1
        FROM e01_factura
        WHERE nro_factura = (%s)
        """,
        (receipt_id,),
    )
    receipt = await acur.fetchone()
    if receipt:
        return True

    return False


async def receipt_exists(receipt_id: int) -> bool:
    async with PsycopgCursor() as (aconn, acur):
        return await _receipt_exists(receipt_id, aconn, acur)


async def get_receipt_details(receipt_id: int):
    async with PsycopgCursor() as (aconn, acur):
        await acur.execute(
            """
                SELECT
                    cantidad, codigo_producto, precio
                FROM  e01_detalle_factura NATURAL JOIN e01_producto
                WHERE nro_factura = (%s)
                """,
            (receipt_id,),
        )
        return await acur.fetchall()


async def get_receipts() -> list[
    tuple[str, int, float], str, int, float
] | tuple[str, int, float]:
    async with PsycopgCursor() as (aconn, acur):
        await acur.execute(
            """
            SELECT
                nro_factura, fecha, iva
            FROM  e01_factura
            """
        )

        return await acur.fetchall()


async def get_receipt_by_id(
    receipt_id: int,
) -> list[tuple[str, int, float], str, int, float] | tuple[str, int, float]:
    async with PsycopgCursor() as (aconn, acur):
        await acur.execute(
            """
            SELECT
                nro_factura, fecha, iva
            FROM  e01_factura
            WHERE nro_factura = (%s)
            """,
            (receipt_id,),
        )

        return await acur.fetchone()


if __name__ == "__main__":
    print("This file is not supposed to be run manually.")
    print("Use run_api.sh or 'uvicorn main:app --reload' instead")
    sys.exit(1)
