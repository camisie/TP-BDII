#!/usr/bin/env python3

import sys

from collections.abc import Callable

from fastapi import HTTPException

from persistence import receipt as receiptDao


def calculate_total(price: int, amount: int, iva: float) -> tuple[int, int]:
    total_no_tax = price * amount
    total_with_tax = total_no_tax * (1 + iva / 100)
    return (total_no_tax, total_with_tax)


async def _receipt_return(
    rows: list[tuple[str, int, float], str, int, float] | tuple[str, int, float],
    details_callback: Callable[
        [int], list[tuple[str, int, float], str, int, float] | tuple[str, int, float]
    ],
) -> dict:
    if not rows:
        return {}

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
            (total_no_tax, total_with_tax) = calculate_total(
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


async def get_receipts() -> dict:
    receipts = await receiptDao.get_receipts()
    return await _receipt_return(receipts, receiptDao.get_receipt_details)


async def get_receipt_by_id(receipt_id: int) -> dict:
    receipt = await receiptDao.get_receipt_by_id(receipt_id)

    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found")

    return await _receipt_return(receipt, receiptDao.get_receipt_details)


if __name__ == "__main__":
    print("This file is not supposed to be run manually.")
    print("Use run_api.sh or 'uvicorn main:app --reload' instead")
    sys.exit(1)
