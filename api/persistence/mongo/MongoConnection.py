#!/usr/bin/env python3

import sys

from typing import Any, Dict

from pymongo import MongoClient


class MongoConnection:
    def __init__(
        self,
        collection: str,
        db_name: str = "e01",
        host: str = "localhost",
        port: int = 27017,
    ):
        self.host = host
        self.port = port
        self.db_name = db_name

        self.client: MongoClient[Dict[str, Any]] = MongoClient(host, port)
        self.db = self.client[self.db_name]
        self.collection = self.get_collection(collection)

    def get_collection(self, collection: str):
        if not collection:
            raise RuntimeError("Empty collection")

        return self.db[collection]


if __name__ == "__main__":
    print("This file is not supposed to be run manually.")
    print("Use run_api.sh or 'uvicorn main:app --reload' instead")
    sys.exit(1)
