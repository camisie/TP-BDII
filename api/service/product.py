#!/usr/bin/env python3

import sys

from fastapi import HTTPException

from persistence.model.Product import Product
from persistence import product as productDao


async def _product_return(
    rows: list[tuple[str, int, float], str, int, float] | tuple[str, int, float]
) -> dict:
    if not rows:
        return {}

    product_columns = [
        "id",
        "brand",
        "name",
        "description",
        "price",
        "stock",
    ]

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


async def get_products() -> dict:
    products = await productDao.get_products()
    return await _product_return(products)


async def get_product_by_id(product_id: int) -> dict:
    product = await productDao.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return await _product_return(product)


async def create_product(product: Product) -> dict:
    new_product_id = await productDao.create_product(product)

    return await get_product_by_id(new_product_id)


async def update_product_by_id(product_id: int, new_product: Product) -> dict:
    if not await productDao.product_exists(product_id):
        raise HTTPException(status_code=404, detail="Product not found")

    await productDao.update_product_by_id(product_id, new_product)

    return await get_product_by_id(product_id)


async def delete_product(product_id: int) -> dict:
    await productDao.delete_product(product_id)
    return {}


if __name__ == "__main__":
    print("This file is not supposed to be run manually.")
    print("Use run_api.sh or 'uvicorn main:app --reload' instead")
    sys.exit(1)
