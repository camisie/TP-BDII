// 1
db.facturas.aggregate([
    {
        $project: {
            nro_factura: 1,
            fecha: 1
        }
    },
    {
        $sort: {
            fecha: 1
        }
    },
    {
        $out: "Vista_FacturasOrdenadas"
    }
])

// 2
db.productos.aggregate([
    {
        $lookup: {
            from: "detalle_factura",
            localField: "codigo_producto",
            foreignField: "codigo_producto",
            as: "detalle_factura"
        }
    },
    {
        $match: {
            "detalle_factura": { $size: 0 }
        }
    },
    {
        $project: {
            _id: 0,
            codigo_producto: 1,
            marca: 1,
            nombre: 1,
            descripcion: 1
        }
    },
    {
        $out: "Vista_ProductosNoFacturados"
    }
])