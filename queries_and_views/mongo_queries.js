const { MongoClient } = require("mongodb");
const fs = require("fs");

const mongo_host = process.env.MONGO_HOST || "localhost";
const mongo_port = process.env.MONGO_PORT || 27017;
const uri = `mongodb://${mongo_host}:${mongo_port}`;
const client = new MongoClient(uri);

async function main() {
    await client.connect();
    const queriesArray = [query1, query2, query3, query4, query5, query6, query7, query8, query9, query10]
    await Promise.all(queriesArray.map(async (query) => query()))
    client.close();
}


const query1 = async () => {
    const db = client.db("e01");
    const result = await db.collection("clientes").find(
    { nombre: "Wanda", apellido: "Baker" })
    .project({ _id: 0, nro_cliente: 1, telefono: 1 })
    .toArray()

    fs.writeFileSync("query1output.json", JSON.stringify(result))
}

const query2 = async () => {
    const db = client.db("e01");
    const result = await db.collection("clientes").aggregate([
        {
            $lookup: {
                "from": "facturas",
                "localField": "nro_cliente",
                "foreignField": "nro_cliente",
                "as": "facturas"
            }
        },
        {
            "$match": { "facturas": { "$exists": true, "$ne": [] } }
        },
        {
            "$project": { "facturas": 0 }
        }
    ]).toArray()
    fs.writeFileSync("query2output.json", JSON.stringify(result))
}

const query3 = async () => {
    const db = client.db("e01");
    const result = await db.collection("clientes").aggregate([
        {
            "$lookup": {
                "from": "facturas",
                "localField": "nro_cliente",
                "foreignField": "nro_cliente",
                "as": "facturas"
            }
        },
        {
            "$match": { "facturas": { "$exists": true, "$eq": [] } }
        },
        {
            "$project": { "facturas": 0 }
        }
    ]).toArray()
    fs.writeFileSync("query3output.json", JSON.stringify(result))

}

const query4 = async () => {
    const db = client.db("e01");
    const result = await db.collection("productos").aggregate([
        {
            "$lookup": {
                "from": "facturas",
                "localField": "codigo_producto",
                "foreignField": "detalles.codigo_producto",
                "as": "facturas"
            }
        },
        {
            "$match": { "facturas": { "$exists": true, "$ne": [] } }
        },
        {
            "$project": { "facturas": 0 }
        }

    ]).toArray()
    fs.writeFileSync("query4output.json", JSON.stringify(result))
}

const query5 = async () => {
    const db = client.db("e01");
    const result = await db.collection("clientes").find({}).toArray()
    fs.writeFileSync("query5output.json", JSON.stringify(result))
}

const query6 = async () => {
    const db = client.db("e01");
    const result = await db.collection("facturas").aggregate([
        {
            "$group": {
                "_id": "$nro_cliente",
                "total": { "$sum": 1 }
            }
        },
        {
            "$lookup": {
                "from": "clientes",
                "localField": "_id",
                "foreignField": "nro_cliente",
                "as": "cliente_info"
            }
        },
        {
            "$unwind": {"path": "$cliente_info", "preserveNullAndEmptyArrays": true}
        },
        {
            "$project": {
                "_id": 0,
                "cliente_info": {
                    nro_cliente: { $ifNull: ["$_id","NULL"] },
                    nombre: { $ifNull: ["$cliente_info.nombre","NULL"] },
                    apellido: { $ifNull: ["$cliente_info.apellido","NULL"] },
                    direccion: { $ifNull: ["$cliente_info.direccion","NULL"] },
                    activo: { $ifNull: ["$cliente_info.activo","NULL"] },
                    telefono: { $ifNull: ["$cliente_info.telefono","NULL"] },
                    total_facturas: "$total"
                }
            }
        }
    ]).toArray()
    fs.writeFileSync("query6output.json", JSON.stringify(result))
}

const query7 = async () => {
    const db = client.db("e01");
    const result = await db.collection("facturas").aggregate([
        {
            "$lookup": {
                "from": "clientes",
                "localField": "nro_cliente",
                "foreignField": "nro_cliente",
                "as": "cliente_info"
            }
        },
        {
            "$match": { "cliente_info.nombre": "Pandora", "cliente_info.apellido": "Tate" }
        },
        {
            "$project": { "_id": 0, "cliente_info": 0, "detalles": 0 }
        }
    ]).toArray()

    fs.writeFileSync("query7output.json", JSON.stringify(result))
}

const query8 = async () => {
    const db = client.db("e01");
    const result = await db.collection("facturas").aggregate([
        {
            "$lookup": {
                "from": "productos",
                "localField": "detalles.codigo_producto",
                "foreignField": "codigo_producto",
                "as": "productos"
            }
        },
        {
            "$match": { "productos.marca": "In Faucibus Inc." }
        },
        {
            "$project": { "_id": 0, "detalles": 0, "productos": 0 }
        }
    ]).toArray()

    fs.writeFileSync("query8output.json", JSON.stringify(result))
}

const query9 = async () => {
    const db = client.db("e01");
    const result = await db.collection("clientes").aggregate([
        {
            "$unwind": "$telefono"
        },
        {
            "$project": {
                "_id": 0,
                "telefono": "$telefono",
                "info_cliente": {
                    "nro_cliente": "$nro_cliente",
                    "nombre": "$nombre",
                    "apellido": "$apellido",
                    "direccion": "$direccion",
                    "activo": "$activo",
                    // "telefono": 0
                }
            }
        }
    ]).toArray()
    fs.writeFileSync("query9output.json", JSON.stringify(result))
}

const query10 = async () => {
    const db = client.db("e01");
    const result = await db.collection("clientes").aggregate([
        {
            "$lookup": {
                "from": "facturas",
                "localField": "nro_cliente",
                "foreignField": "nro_cliente",
                "as": "facturas"
            }
        },
        {
            "$project": {
                "_id": 0,
                "nombre": "$nombre",
                "apellido": "$apellido",
                "total_gastado": { "$sum": "$facturas.total_con_iva" }
            }
        }
    ]).toArray()
    fs.writeFileSync("query10output.json", JSON.stringify(result))
}

main()
