#!/usr/bin/env python3

from sys import exit
from pydantic import BaseModel


class Client(BaseModel):
    nombre: str
    apellido: str
    direccion: str
    activo: int


class ClientId(BaseModel):
    id: str
    nombre: str
    apellido: str
    direccion: str
    activo: int


if __name__ == "__main__":
    print("This file is not supposed to be run manually.")
    print("Use run_api.sh or 'uvicorn main:app --reload' instead")
    exit(1)
