import asyncio
import os
import psycopg as pg
from pymongo import MongoClient
from datetime import datetime

psql_params = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}

mongo_connection_string = f"mongodb://{os.getenv('MONGO_HOST')}:{os.getenv('MONGO_PORT')}/"


async def main():
    asyncio.create_task(migrate_products())
    asyncio.create_task(migrate_clients())
    asyncio.create_task(migrate_facturas())
    print("Starting migration")


async def migrate_products():
    connection = pg.connect(**psql_params)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM e01_producto")
    columns = [desc[0] for desc in cursor.description]
    result = [dict(zip(columns, row)) for row in cursor]
    cursor.close()
    connection.close()
    upload_products_to_mongo(result)


def upload_products_to_mongo(products):
    client = MongoClient(mongo_connection_string)
    db = client.e01
    collection = db.productos
    collection.insert_many(products)
    client.close()


async def migrate_clients():
    connection = pg.connect(**psql_params)
    cursor = connection.cursor()
    cursor.execute("SELECT C.*, json_agg(json_build_object('codigo_area', T.codigo_area, 'numero', T.nro_telefono, 'tipo', T.tipo)) as telefono "
                   "FROM E01_CLIENTE C LEFT JOIN E01_TELEFONO T ON C.nro_cliente = T.nro_cliente "
                   "GROUP BY C.nro_cliente")
    columns = [desc[0] for desc in cursor.description]
    result = [dict(zip(columns, row)) for row in cursor]
    for row in result:
        if row['telefono'][0]['numero'] is None:
            row['telefono'].clear()
    cursor.close()
    connection.close()
    upload_clients_to_mongo(result)


def upload_clients_to_mongo(clients):
    client = MongoClient(mongo_connection_string)
    db = client.e01
    collection = db.clientes
    collection.insert_many(clients)
    client.close()


async def migrate_facturas():
    connection = pg.connect(**psql_params)
    cursor = connection.cursor()
    cursor.execute("SELECT F.*, json_agg(json_build_object('nro_item', D.nro_item, 'cantidad', D.cantidad, 'codigo_producto', D.codigo_producto)) as detalles"
                   " FROM e01_factura as F LEFT JOIN e01_detalle_factura AS D ON F.nro_factura = D.nro_factura GROUP BY F.nro_factura")
    columns = [desc[0] for desc in cursor.description]
    result = [dict(zip(columns, row)) for row in cursor]
    for row in result:
        if len(row['detalles']) == 1 and row['detalles'][0]['cantidad'] is None:
            row['detalles'].clear()
        row['fecha'] = datetime.combine(row['fecha'], datetime.min.time())
    cursor.close()
    connection.close()
    upload_facturas_to_mongo(result)


def upload_facturas_to_mongo(facturas):
    client = MongoClient(mongo_connection_string)
    db = client.e01
    collection = db.facturas
    collection.insert_many(facturas)
    client.close()


if __name__ == "__main__":
    asyncio.run(main())
