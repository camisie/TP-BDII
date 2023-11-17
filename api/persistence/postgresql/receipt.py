#!/usr/bin/env python3

import sys

from .PsycopgCursor import PsycopgCursor

from ..model.Product import Product
from ..model.Receipt import ReceiptDetail, ReceiptId


async def _get_receipt_details(receipt_id: int | str):
    async with PsycopgCursor() as (aconn, acur):
        await acur.execute(
            """
            SELECT
                nro_item, cantidad,
                marca, nombre, descripcion, precio, stock
            FROM  e01_detalle_factura NATURAL JOIN e01_producto
            WHERE nro_factura = (%s)
            """,
            (receipt_id,),
        )
        results = await acur.fetchall()

        receipt_details: list[ReceiptDetail] = []

        for result in results:
            product_dict = {
                "marca": result[2],
                "nombre": result[3],
                "descripcion": result[4],
                "precio": float(result[5]),
                "stock": int(result[6]),
            }
            receipt_dict = {
                "nro_item": int(result[0]),
                "cantidad": int(result[1]),
                "producto": Product(**product_dict),
            }
            receipt_details.append(receipt_dict)

        return receipt_details


async def _map_to_receipt_id(row) -> ReceiptId | None:
    if not row:
        return None

    columns = list(ReceiptId.__annotations__.keys())
    columns.remove("nro_factura")

    receipt = {}
    for key, value in zip(columns, row):
        if key == "fecha":
            value = str(value)

        receipt[key] = value

    receipt["id"] = str(receipt.get("id", ""))
    receipt["nro_factura"] = int(receipt.get("id", 0))

    receipt_details = await _get_receipt_details(receipt["nro_factura"])

    return ReceiptId(detalles=receipt_details, **receipt)


async def _receipt_exists(receipt_id: int | str, aconn, acur) -> bool:
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


async def receipt_exists(receipt_id: int | str) -> bool:
    async with PsycopgCursor() as (aconn, acur):
        return await _receipt_exists(receipt_id, aconn, acur)


async def get_receipts() -> list[ReceiptId] | None:
    async with PsycopgCursor() as (aconn, acur):
        await acur.execute(
            """
            SELECT
                nro_factura, fecha, total_sin_iva, iva, total_con_iva, nro_cliente
            FROM  e01_factura
            """
        )

        result = await acur.fetchall()
        if not result:
            return None

        mapped = [await _map_to_receipt_id(receipt) for receipt in result]
        return [receipt for receipt in mapped if receipt is not None]


async def get_receipt_by_id(receipt_id: int | str) -> ReceiptId:
    async with PsycopgCursor() as (aconn, acur):
        await acur.execute(
            """
            SELECT
                nro_factura, fecha, total_sin_iva, iva, total_con_iva, nro_cliente
            FROM  e01_factura
            WHERE nro_factura = (%s)
            """,
            (receipt_id,),
        )

        result = await acur.fetchone()
        if not result:
            return None

        mapped = await _map_to_receipt_id(result)
        return mapped


if __name__ == "__main__":
    print("This file is not supposed to be run manually.")
    print("Use run_api.sh or 'uvicorn main:app --reload' instead")
    sys.exit(1)
