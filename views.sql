-- 1
CREATE VIEW Vista_FacturasOrdenadas AS
SELECT *
FROM E01_FACTURA
ORDER BY fecha;

-- 2
CREATE VIEW Vista_ProductosNoFacturados AS
SELECT P.*
FROM E01_PRODUCTO P
LEFT JOIN E01_DETALLE_FACTURA DF ON P.codigo_producto = DF.codigo_producto
WHERE DF.codigo_producto IS NULL;
