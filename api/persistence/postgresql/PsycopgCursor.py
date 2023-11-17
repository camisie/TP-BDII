#!/usr/bin/env python3

import sys
from os import environ

import psycopg


class PsycopgCursor:
    def __init__(self):
        self.psql_params = {
            "dbname": environ.get("PSQL_DB_NAME", "e01"),
            "user": environ.get("PSQL_USER", "postgres"),
            "password": environ.get("PSQL_PASSWORD", "12345"),
            "host": environ.get("PSQL_HOST", "127.0.0.1"),
            "port": environ.get("PSQL_PORT", "5432"),
        }

    async def __aenter__(self):
        self.aconn = await psycopg.AsyncConnection.connect(**self.psql_params)
        self.cursor = self.aconn.cursor()
        return (self.aconn, self.cursor)

    async def __aexit__(self, exception_type, exception_value, exception_traceback):
        await self.aconn.commit()
        await self.cursor.close()
        await self.aconn.close()


if __name__ == "__main__":
    print("This file is not supposed to be run manually.")
    print("Use run_api.sh or 'uvicorn main:app --reload' instead")
    sys.exit(1)
