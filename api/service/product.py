#!/usr/bin/env python3

import sys
from os import environ

from fastapi import HTTPException

from persistence.model.Product import Product, ProductId

if environ.get("API_DB", None) == "mongodb":
    from persistence.mongo import product as productDao
else:
    from persistence.postgresql import product as productDao


async def _product_return(rows: list[ProductId] | ProductId) -> dict:
    if not rows:
        return {}

    products = {"products": []}

    if isinstance(rows, ProductId):
        return rows.model_dump()

    products["products"] = rows
    return products


async def get_products():
    products = await productDao.get_products()
    return await _product_return(products)


async def get_product_by_id(product_id: int | str):
    product = await productDao.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return await _product_return(product)


async def create_product(product: Product):
    new_product_id = await productDao.create_product(product)

    return await get_product_by_id(new_product_id)


async def update_product_by_id(product_id: int | str, new_product: Product):
    if not await productDao.product_exists(product_id):
        raise HTTPException(status_code=404, detail="Product not found")

    await productDao.update_product_by_id(product_id, new_product)

    return await get_product_by_id(product_id)


async def delete_product(product_id: int | str):
    await productDao.delete_product(product_id)
    return {}


if __name__ == "__main__":
    print("This file is not supposed to be run manually.")
    print("Use run_api.sh or 'uvicorn main:app --reload' instead")
    sys.exit(1)
