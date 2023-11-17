#!/usr/bin/env python3

from sys import exit

from pydantic import BaseModel

from .Product import Product


class ReceiptDetail(BaseModel):
    nro_item: int
    cantidad: int
    producto: Product


class ReceiptId(BaseModel):
    id: str
    nro_factura: int
    fecha: str
    total_sin_iva: float
    iva: float
    total_con_iva: float
    nro_cliente: int
    detalles: list[ReceiptDetail]


class Receipt(BaseModel):
    fecha: str
    total_sin_iva: float
    iva: float
    total_con_iva: float
    nro_cliente: int
    detalles: list[ReceiptDetail]


if __name__ == "__main__":
    print("This file is not supposed to be run manually.")
    print("Use run_api.sh or 'uvicorn main:app --reload' instead")
    exit(1)
