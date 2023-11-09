// 1
db.clientes.aggregate([
  {
    $match: { nombre: "Wanda", apellido: "Baker" }
  },
  {
    $lookup: {
      from: "telefonos",
      localField: "nro_cliente",
      foreignField: "nro_cliente",
      as: "telefonos"
    }
  },
  {
    $unwind: "$telefonos"
  },
  {
    $project: {
      _id: 0,
      nro_telefono: "$telefonos.nro_telefono",
      nro_cliente: 1
    }
  }
]);

// 2
db.clientes.aggregate([
  {
    $lookup: {
      from: "facturas",
      localField: "nro_cliente",
      foreignField: "nro_cliente",
      as: "facturas"
    }
  },
  {
    $match: { "facturas": { $exists: true, $ne: [] } }
  }
]);

// 3
db.clientes.aggregate([
  {
    $lookup: {
      from: "facturas",
      localField: "nro_cliente",
      foreignField: "nro_cliente",
      as: "facturas"
    }
  },
  {
    $match: { "facturas": { $exists: false } }
  }
]);

// 4
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
    $match: { "detalle_factura": { $exists: true, $ne: [] } }
  }
]);

// 5
db.clientes.aggregate([
  {
    $lookup: {
      from: "telefonos",
      localField: "nro_cliente",
      foreignField: "nro_cliente",
      as: "telefonos"
    }
  }
]);

// 6
db.clientes.aggregate([
  {
    $lookup: {
      from: "facturas",
      localField: "nro_cliente",
      foreignField: "nro_cliente",
      as: "facturas"
    }
  },
  {
    $project: {
      _id: 0,
      nro_cliente: 1,
      nombre: 1,
      apellido: 1,
      direccion: 1,
      activo: 1,
      cantidad_facturas: { $size: { $ifNull: ["$facturas", []] } }
    }
  }
]);

// 7
db.facturas.aggregate([
  {
    $lookup: {
      from: "clientes",
      localField: "nro_cliente",
      foreignField: "nro_cliente",
      as: "cliente"
    }
  },
  {
    $match: { "cliente.nombre": "Pandora", "cliente.apellido": "Tate" }
  }
]);

// 8
db.facturas.aggregate([
  {
    $lookup: {
      from: "detalle_factura",
      localField: "nro_factura",
      foreignField: "nro_factura",
      as: "detalle_factura"
    }
  },
  {
    $unwind: "$detalle_factura"
  },
  {
    $lookup: {
      from: "productos",
      localField: "detalle_factura.codigo_producto",
      foreignField: "codigo_producto",
      as: "productos"
    }
  },
  {
    $match: { "productos.marca": "In Faucibus Inc." }
  }
]);

// 9
db.clientes.aggregate([
  {
    $lookup: {
      from: "telefonos",
      localField: "nro_cliente",
      foreignField: "nro_cliente",
      as: "telefonos"
    }
  },
  {
    $unwind: { path: "$telefonos", preserveNullAndEmptyArrays: true }
  }
]);

// 10
db.clientes.aggregate([
  {
    $lookup: {
      from: "facturas",
      localField: "nro_cliente",
      foreignField: "nro_cliente",
      as: "facturas"
    }
  },
  {
    $unwind: "$facturas"
  },
  {
    $group: {
      _id: "$_id",
      nombre: { $first: "$nombre" },
      apellido: { $first: "$apellido" },
      gasto_total: { $sum: "$facturas.total_con_iva" }
    }
  }
]);
