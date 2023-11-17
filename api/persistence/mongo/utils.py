#!/usr/bin/env python3

import sys

from bson.objectid import ObjectId

from .MongoConnection import MongoConnection


def get_id(
    id: int | str | ObjectId, connection: MongoConnection, alternative_id: str
) -> ObjectId | None:
    if isinstance(id, ObjectId):
        return id

    if isinstance(id, int) or id.isdigit():
        result = connection.collection.find_one({alternative_id: int(id)})
        if not result:
            return None

        return result.get("_id", None)

    return ObjectId(id)


if __name__ == "__main__":
    print("This file is not supposed to be run manually.")
    print("Use run_api.sh or 'uvicorn main:app --reload' instead")
    sys.exit(1)
