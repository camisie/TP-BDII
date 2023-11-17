#!/usr/bin/env python3

import sys

from .PsycopgCursor import PsycopgCursor

from ..model.Product import Product, ProductId


def _map_to_productid(row) -> ProductId | None:
    if not row:
        return None

    columns = list(ProductId.__annotations__.keys())

    product = dict(zip(columns, row))
    product["id"] = str(product.get("id", ""))
    return ProductId(**product)


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


async def get_products() -> list[ProductId] | None:
    async with PsycopgCursor() as (aconn, acur):
        await acur.execute(
            """
            SELECT
                 codigo_producto, marca, nombre, descripcion, precio, stock
            FROM e01_producto 
            """
        )

        result = await acur.fetchall()
        if not result:
            return None

        mapped = [_map_to_productid(product) for product in result]
        return [product for product in mapped if product is not None]


async def get_product_by_id(
    product_id: int | str,
) -> ProductId | None:
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

        result = await acur.fetchone()
        if not result:
            return None

        product = _map_to_productid(result)
        return product


async def create_product(product: Product) -> int:
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
                product.marca,
                product.nombre,
                product.descripcion,
                product.precio,
                product.stock,
            ),
        )
        await aconn.commit()

        inserted_id = await acur.fetchone()
        return inserted_id[0]


async def update_product_by_id(product_id: int, new_product: Product) -> int:
    async with PsycopgCursor() as (aconn, acur):
        await aconn.execute(
            """
            UPDATE e01_producto
            SET marca = %(brand)s, nombre = %(name)s, descripcion = %(description)s,
                precio = %(price)s, stock = %(stock)s
            WHERE codigo_producto = %(id)s
            """,
            {
                "id": product_id,
                "brand": new_product.marca,
                "name": new_product.nombre,
                "description": new_product.descripcion,
                "price": new_product.precio,
                "stock": new_product.stock,
            },
        )

        await aconn.commit()

        return product_id


async def delete_product(product_id: int) -> None:
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


if __name__ == "__main__":
    print("This file is not supposed to be run manually.")
    print("Use run_api.sh or 'uvicorn main:app --reload' instead")
    sys.exit(1)
