#!/usr/bin/env python3

import sys
from os import environ

from typing import Any, Dict

from pymongo import MongoClient

from bson.objectid import ObjectId


class MongoConnection:
    def __init__(
        self,
        collection: str,
        db_name: str = "e01",
        host: str = environ.get("MONGO_HOST", "localhost"),
        port: int | str = environ.get("MONGO_PORT", 27017),
    ):
        self.host = host
        self.port = int(port)
        self.db_name = db_name

        self.client: MongoClient[Dict[str, Any]] = MongoClient(host, int(port))
        self.db = self.client[self.db_name]
        self.collection = self.get_collection(collection)

    def get_collection(self, collection: str):
        if not collection:
            raise RuntimeError("Empty collection")

        return self.db[collection]

    def get_id(self, id: int | str | ObjectId, alternative_id: str) -> ObjectId | None:
        if isinstance(id, ObjectId):
            return id

        if isinstance(id, int) or id.isdigit():
            result = self.collection.find_one({alternative_id: int(id)})
            if not result:
                return None

            return result.get("_id", None)

        return ObjectId(id)


if __name__ == "__main__":
    print("This file is not supposed to be run manually.")
    print("Use run_api.sh or 'uvicorn main:app --reload' instead")
    sys.exit(1)
