#!/usr/bin/env python3

import sys

from collections.abc import Awaitable, Callable

from fastapi import HTTPException
from pydantic import BaseModel


from .PsycopgCursor import PsycopgCursor


# class ReceiptDetail(BaseModel):
#     amount: int
#     product_id: int
#
#
# class Receipt(BaseModel):
#     date: str
#     total_no_tax: float
#     iva: float
#     total: float
#     client_id: int
#     details: list[ReceiptDetail]


def calculate_total(price: int, amount: int, iva: float) -> tuple[int, int]:
    total_no_tax = price * amount
    total_with_tax = total_no_tax * (1 + iva / 100)
    return (total_no_tax, total_with_tax)


async def _receipt_return(fetch: Awaitable, details_callback: Callable) -> dict:
    receipt_columns = [
        "id",
        "date",
        "iva",
        "client_id",
    ]
    details_columns = [
        "amount",
        "product_id",
    ]

    rows = await fetch()
    if not rows:
        return {}

    receipts = {"receipts": []}
    try:
        receipts["receipts"] = [
            dict(zip(receipt_columns, map(str, row))) for row in rows
        ]

    except TypeError:
        receipts["receipts"] = [dict(zip(receipt_columns, map(str, rows)))]

    for receipt in receipts["receipts"]:
        rows = await details_callback(receipt[receipt_columns[0]])
        if not rows:
            continue

        receipt["details"] = []

        for row in rows:
            details_dict = {}
            for index, column in enumerate(details_columns):
                details_dict[column] = str(row[index])

            # Calculate totals
            (total_with_tax, total_no_tax) = calculate_total(
                row[2], row[0], float(receipt["iva"])
            )

            # Prices with four decimal places, maximum
            receipt["total_no_tax"] = str(round(total_no_tax, 2))
            receipt["total"] = str(round(total_with_tax, 2))

            # Add details
            receipt["details"].append(details_dict)

    if len(receipts["receipts"]) == 1:
        return receipts["receipts"][0]

    return receipts


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


async def get_receipts() -> dict:
    async with PsycopgCursor() as (aconn, acur):

        async def callback(id: int):
            await acur.execute(
                """
                SELECT
                    cantidad, codigo_producto, precio
                FROM  e01_detalle_factura NATURAL JOIN e01_producto
                WHERE nro_factura = (%s)
                """,
                (id,),
            )
            return await acur.fetchall()

        await acur.execute(
            """
            SELECT
                nro_factura, fecha, iva
            FROM  e01_factura
            """
        )

        return await _receipt_return(acur.fetchall, callback)


async def get_receipt_by_id(receipt_id: int) -> dict:
    async with PsycopgCursor() as (aconn, acur):

        async def callback(id: int):
            await acur.execute(
                """
                SELECT
                    cantidad, codigo_producto, precio
                FROM  e01_detalle_factura NATURAL JOIN e01_producto
                WHERE nro_factura = (%s)
                """,
                (id,),
            )
            return await acur.fetchall()

        await acur.execute(
            """
            SELECT
                nro_factura, fecha, iva
            FROM  e01_factura
            WHERE nro_factura = (%s)
            """,
            (receipt_id,),
        )

        receipt = await _receipt_return(acur.fetchone, callback)
        if not receipt:
            raise HTTPException(status_code=404, detail="Receipt not found")

        return receipt


if __name__ == "__main__":
    print("This file is not supposed to be run manually.")
    print("Use run_api.sh or 'uvicorn main:app --reload' instead")
    sys.exit(1)
