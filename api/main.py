#!/usr/bin/env python3

import sys


from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

import service.client as client_service
from service.client import Client

import service.phone as phone_service
from service.phone import Phone

import service.product as product_service
from service.product import Product


app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
      <head>
        <title>API :)</title>
      </head>
      <body>
        <h1>PostgreSQL API</h1>
        <p>Go to <a href="/docs">/docs</a> for the Swagger UI</p>
      </body>
    </html>
    """


# =============== Clients ===============


@app.get("/clients")
async def get_clients():
    return await client_service.get_clients()


@app.post("/clients")
async def create_client(client: Client):
    return await client_service.create_client(client)


@app.get("/clients/{client_id}")
async def get_client(client_id: int):
    return await client_service.get_client_by_id(client_id)


@app.put("/clients/{client_id}")
async def update_client(client_id: int, client: Client):
    return await client_service.update_client_by_id(client_id, client)


@app.delete("/clients/{client_id}")
async def remove_client(client_id: int):
    return await client_service.delete_client(client_id)


# =============== Phones ===============


@app.get("/phones")
async def get_phones():
    return await phone_service.get_phones()


@app.get("/phones/{client_id}")
async def get_phone_by_client_id(client_id: int):
    return await phone_service.get_phone_by_client_id(client_id)


@app.put("/phones/{client_id}")
async def create_or_update_phone(client_id: int, phone: Phone):
    return await phone_service.update_phone(client_id, phone)


@app.post("/phones/{client_id}")
async def create_phone(client_id: int, phone: Phone):
    return await phone_service.create_phone(client_id, phone)


@app.delete("/phones/{client_id}")
async def remove_phone(client_id: int, code: int | None, number: int | None):
    if code and number:
        return await phone_service.delete_phone(client_id, code, number)
    if not code and not number:
        return await phone_service.delete_phones(client_id)

    raise HTTPException(
        status_code=400,
        detail="Provide both code and number to remove a specific phone number,"
        " or neither to remove all numbers from client",
    )


# =============== Products ===============


@app.get("/products")
async def get_products():
    return await product_service.get_products()


@app.post("/products")
async def create_product(product: Product):
    return await product_service.create_product(product)


@app.get("/products/{product_id}")
async def get_product(product_id: int):
    return await product_service.get_product_by_id(product_id)


@app.put("/products/{product_id}")
async def update_product(product_id: int, product: Product):
    return await product_service.update_product_by_id(product_id, product)


@app.delete("/products/{product_id}")
async def remove_product(product_id: int):
    return await product_service.delete_product(product_id)


if __name__ == "__main__":
    print("This file is not supposed to be run manually.")
    print("Use run_api.sh or 'uvicorn main:app --reload' instead")
    sys.exit(1)
