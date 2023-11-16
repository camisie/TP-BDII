#!/usr/bin/env python3

import sys

import psycopg


class PsycopgCursor:
    def __init__(self):
        pass

    async def __aenter__(self):
        self.aconn = await psycopg.AsyncConnection.connect("dbname=bd2-tpo")
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
