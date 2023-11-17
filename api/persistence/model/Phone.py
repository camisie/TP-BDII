#!/usr/bin/env python3

from sys import exit

from pydantic import BaseModel


class Phone(BaseModel):
    codigo_area: int
    numero: int
    tipo: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "codigo_area": "11",
                    "numero": "12345678",
                    "tipo": "X",
                }
            ]
        }
    }


if __name__ == "__main__":
    print("This file is not supposed to be run manually.")
    print("Use run_api.sh or 'uvicorn main:app --reload' instead")
    exit(1)
