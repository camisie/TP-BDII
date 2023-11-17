#!/usr/bin/env python3

import sys
from typing import Any

from bson.objectid import ObjectId

from .MongoConnection import MongoConnection

from .product import get_product_by_id

from ..model.Receipt import ReceiptId


def _get_id(
    id: int | str | ObjectId,
    connection: MongoConnection,
    alternative_id: str = "nro_factura",
) -> ObjectId | None:
    return connection.get_id(id, alternative_id)


def _get_connection():
    return MongoConnection("facturas")


async def receipt_exists(receipt_id: int | str | ObjectId) -> bool:
    conn = _get_connection()
    id = _get_id(receipt_id, conn)
    if not id:
        return False

    receipt = conn.collection.find_one({"_id": id})
    if receipt:
        return True

    return False


async def _fix_receipt(receipt: dict[str, Any]) -> ReceiptId:
    id = str(receipt.pop("_id"))
    date = str(receipt.pop("fecha"))
    if len(receipt.get("detalles", [])) > 0:
        for detail in receipt["detalles"]:
            code = detail.pop("codigo_producto")
            product_with_id = await get_product_by_id(code)
            if product_with_id:
                detail["producto"] = product_with_id.model_dump()

    return ReceiptId(id=id, fecha=date, **receipt)


async def get_receipts() -> list[ReceiptId]:
    conn = _get_connection()
    receipts = conn.collection.find()

    receipts_list: list[ReceiptId] = []
    for receipt in receipts:
        if receipt.get("id", None):
            receipt.pop("id")

        try:
            receipt_obj = await _fix_receipt(receipt)
            receipts_list.append(receipt_obj)
        except TypeError:
            pass

    return receipts_list


async def get_receipt_by_id(receipt_id: int | str | ObjectId) -> ReceiptId | None:
    conn = _get_connection()
    id = _get_id(receipt_id, conn)
    if not id:
        return None

    receipt = conn.collection.find_one({"_id": id})
    if not receipt:
        return None

    return await _fix_receipt(receipt)


if __name__ == "__main__":
    print("This file is not supposed to be run manually.")
    print("Use run_api.sh or 'uvicorn main:app --reload' instead")
    sys.exit(1)
