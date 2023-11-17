const { MongoClient } = require("mongodb");

const mongo_host = process.env.MONGO_HOST || "localhost";
const mongo_port = process.env.MONGO_PORT || 27017;
const uri = `mongodb://${mongo_host}:${mongo_port}`;
const client = new MongoClient(uri);

async function main() {
    client.connect();
    console.log("Connected successfully to mongo, creating views...");
    const db = client.db("e01");

    await db.createCollection("facturas_ordenadas_por_fecha", { viewOn: "facturas", pipeline: [{ $sort: { fecha: 1 } }] });

    await db.createCollection("productos_sin_facturas", { viewOn: "productos", pipeline: [
        {
            "$lookup": {
                "from": "facturas",
                "localField": "codigo_producto",
                "foreignField": "detalles.codigo_producto",
                "as": "facturas"
            }
        },
        {
            "$match": { "facturas": { "$eq": [] } }
        },
        {
            "$project": { "facturas": 0 }
        }
    ]});

    client.close();
    console.log("Views created successfully");
}

main()
