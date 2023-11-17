#!/usr/bin/env python3

from sys import exit

from pydantic import BaseModel


class ReceiptDetail(BaseModel):
    amount: int
    product_id: int


class Receipt(BaseModel):
    date: str
    total_no_tax: float
    iva: float
    total: float
    client_id: int
    details: list[ReceiptDetail]


if __name__ == "__main__":
    print("This file is not supposed to be run manually.")
    print("Use run_api.sh or 'uvicorn main:app --reload' instead")
    exit(1)
