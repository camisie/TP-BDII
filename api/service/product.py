#!/usr/bin/env python3

import sys

from collections.abc import Awaitable

from fastapi import HTTPException
from pydantic import BaseModel


from .PsycopgCursor import PsycopgCursor


class Product(BaseModel):
    brand: str
    name: str
    description: str
    price: float
    stock: int


async def _product_return(fetch: Awaitable) -> dict:
    product_columns = [
        "id",
        "brand",
        "name",
        "description",
        "price",
        "stock",
    ]

    rows = await fetch()
    if not rows:
        return {}

    products = {"products": []}
    try:
        products["products"] = [
            dict(zip(product_columns, map(str, row))) for row in rows
        ]

    except TypeError:
        products["products"] = [dict(zip(product_columns, map(str, rows)))]

    if len(products["products"]) == 1:
        return products["products"][0]

    return products


async def _product_exists(product_id: int, aconn, acur) -> bool:
    await acur.execute(
        """
        SELECT
            1
        FROM e01_producto AS product
        WHERE product.codigo_producto = (%s)
        """,
        (product_id,),
    )
    product = await acur.fetchone()
    if product:
        return True

    return False


async def product_exists(product_id: int) -> bool:
    async with PsycopgCursor() as (aconn, acur):
        return await _product_exists(product_id, aconn, acur)


async def get_products() -> dict:
    async with PsycopgCursor() as (aconn, acur):
        await acur.execute(
            """
            SELECT
                 codigo_producto, marca, nombre, descripcion, precio, stock
            FROM e01_producto 
            """
        )

        return await _product_return(acur.fetchall)


async def get_product_by_id(product_id: int) -> dict:
    async with PsycopgCursor() as (aconn, acur):
        await acur.execute(
            """
             SELECT
                 codigo_producto, marca, nombre, descripcion, precio, stock
             FROM e01_producto
             WHERE codigo_producto = (%s)
             """,
            (product_id,),
        )

        product = await _product_return(acur.fetchone)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        return product


async def create_product(product: Product) -> dict:
    async with PsycopgCursor() as (aconn, acur):
        await acur.execute(
            """
             INSERT INTO
                 e01_producto (marca, nombre, descripcion, precio, stock)
             VALUES
                 (%s, %s, %s, %s, %s)
             RETURNING
                 codigo_producto
             """,
            (
                product.brand,
                product.name,
                product.description,
                product.price,
                product.stock,
            ),
        )
        await aconn.commit()

        inserted_id = await acur.fetchone()
        inserted_id = inserted_id[0]

        return await get_product_by_id(inserted_id)


async def update_product_by_id(product_id: int, new_product: Product) -> dict:
    async with PsycopgCursor() as (aconn, acur):
        if not await _product_exists(product_id, aconn, acur):
            raise HTTPException(status_code=404, detail="Product not found")

        query = """
            UPDATE e01_producto
            SET marca = %(brand)s, nombre = %(name)s, descripcion = %(description)s,
                precio = %(price)s, stock = %(stock)s
            WHERE codigo_producto = %(id)s
            """

        await aconn.execute(
            query,
            {
                "id": product_id,
                "brand": new_product.brand,
                "name": new_product.name,
                "description": new_product.description,
                "price": new_product.price,
                "stock": new_product.stock,
            },
        )

        await aconn.commit()

        return await get_product_by_id(product_id)


async def delete_product(product_id: int) -> dict:
    async with PsycopgCursor() as (aconn, acur):
        await acur.execute(
            """
             DELETE 
             FROM e01_producto 
             WHERE codigo_producto = (%s)
             """,
            (product_id,),
        )
        await aconn.commit()

        return {}


if __name__ == "__main__":
    print("This file is not supposed to be run manually.")
    print("Use run_api.sh or 'uvicorn main:app --reload' instead")
    sys.exit(1)
