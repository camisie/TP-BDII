#!/usr/bin/env python3

from sys import exit
from pydantic import BaseModel


class Product(BaseModel):
    marca: str
    nombre: str
    descripcion: str
    precio: float
    stock: int


class ProductId(BaseModel):
    id: str
    codigo_producto: int
    marca: str
    nombre: str
    descripcion: str
    precio: float
    stock: int


if __name__ == "__main__":
    print("This file is not supposed to be run manually.")
    print("Use run_api.sh or 'uvicorn main:app --reload' instead")
    exit(1)
