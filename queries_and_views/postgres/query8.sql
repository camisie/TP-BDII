SELECT DISTINCT F.*
FROM E01_FACTURA F
JOIN E01_DETALLE_FACTURA DF ON F.nro_factura = DF.nro_factura
JOIN E01_PRODUCTO P ON DF.codigo_producto = P.codigo_producto
WHERE P.marca = 'In Faucibus Inc.';

