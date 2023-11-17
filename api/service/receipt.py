#!/usr/bin/env python3

import sys

from collections.abc import Callable

from fastapi import HTTPException

from persistence.model.Receipt import Receipt, ReceiptId

# from persistence.postgresql import receipt as receiptDao

from persistence.mongo import receipt as receiptDao


def _calculate_total(price: int, amount: int, iva: float) -> tuple[int, float]:
    total_no_tax = price * amount
    total_with_tax = total_no_tax * (1 + iva / 100)
    return (total_no_tax, total_with_tax)


def _complete_receipt_total(receipt: Receipt):
    for detail in receipt.detalles:
        # Calculate totals
        (total_no_tax, total_with_tax) = _calculate_total(
            detail.producto.precio, detail.cantidad, float(receipt.iva)
        )

        # Prices with four decimal places, maximum
        receipt.total_sin_iva = float(round(total_no_tax, 2))
        receipt.total_con_iva = float(round(total_with_tax, 2))

    return receipt


def _complete_receipts_total(receipts: list[Receipt]):
    return list(map(_complete_receipt_total, receipts))


async def _receipt_return(rows: ReceiptId | list[ReceiptId]) -> dict:
    if not rows:
        return {}

    receipts = {"receipts": []}

    if isinstance(rows, ReceiptId):
        rows = _complete_receipt_total(rows)
        return rows.model_dump()

    if isinstance(rows[0], ReceiptId):
        receipts["receipts"] = _complete_receipts_total(rows)
        return receipts

    return {}


async def get_receipts() -> dict:
    receipts = await receiptDao.get_receipts()
    return await _receipt_return(receipts)


async def get_receipt_by_id(receipt_id: int | str) -> dict:
    receipt = await receiptDao.get_receipt_by_id(receipt_id)

    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found")

    return await _receipt_return(receipt)


if __name__ == "__main__":
    print("This file is not supposed to be run manually.")
    print("Use run_api.sh or 'uvicorn main:app --reload' instead")
    sys.exit(1)
