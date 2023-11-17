#!/usr/bin/env python3

import sys

from bson.objectid import ObjectId

from .MongoConnection import MongoConnection

from ..model.Product import Product, ProductId


def _get_connection():
    return MongoConnection("productos")


def _get_id(id: int | str | ObjectId):
    if isinstance(id, str):
        return ObjectId(id)

    return id


async def product_exists(product_id: int | str | ObjectId) -> bool:
    conn = _get_connection()
    product_id = _get_id(product_id)

    product = conn.collection.find_one({"_id": product_id})
    if product:
        return True

    return False


async def get_products() -> list[ProductId]:
    conn = _get_connection()
    products = conn.collection.find()

    products_list: list[ProductId] = []
    for product in products:
        if product.get("id", None):
            product.pop("id")

        try:
            id = str(product.pop("_id"))
            print(id)
            print(product)
            product_obj = ProductId(id=id, **product)
            products_list.append(product_obj)
        except TypeError:
            pass

    return products_list


async def get_product_by_id(product_id: int | str | ObjectId) -> ProductId | None:
    conn = _get_connection()
    product_id = _get_id(product_id)

    product = conn.collection.find_one({"_id": product_id})

    if not product:
        return None

    id = str(product.pop("_id"))
    product_obj = ProductId(id=id, **product)
    return product_obj


async def create_product(product: Product) -> int:
    conn = _get_connection()
    product_dict = product.model_dump()

    if product_dict.get("id", None):
        product_dict.pop("id")

    product_id = conn.collection.insert_one(product_dict).inserted_id

    return product_id


async def update_product_by_id(
    product_id: int | str | ObjectId, new_product: Product
) -> int | str | ObjectId | None:
    conn = _get_connection()
    product_id = _get_id(product_id)

    conn.collection.update_one({"_id": product_id}, {"$set": new_product.model_dump()})
    return product_id


async def delete_product(product_id: int | str | ObjectId) -> None:
    conn = _get_connection()
    product_id = _get_id(product_id)

    conn.collection.delete_one({"_id": product_id})

    return None


if __name__ == "__main__":
    print("This file is not supposed to be run manually.")
    print("Use run_api.sh or 'uvicorn main:app --reload' instead")
    sys.exit(1)
