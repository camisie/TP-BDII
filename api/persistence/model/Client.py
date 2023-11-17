#!/usr/bin/env python3

from sys import exit
from pydantic import BaseModel

from .Phone import Phone


class Client(BaseModel):
    nombre: str
    apellido: str
    direccion: str
    activo: int
    telefono: list[Phone]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "nombre": "pedro",
                    "apellido": "lopez",
                    "direccion": "su casa 123",
                    "activo": 3,
                    "telefono": [],
                }
            ]
        }
    }


class ClientId(BaseModel):
    id: str
    nro_cliente: int
    nombre: str
    apellido: str
    direccion: str
    activo: int
    telefono: list[Phone]


if __name__ == "__main__":
    print("This file is not supposed to be run manually.")
    print("Use run_api.sh or 'uvicorn main:app --reload' instead")
    exit(1)
