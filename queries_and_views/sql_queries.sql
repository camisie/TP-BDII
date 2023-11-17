-- 1
SELECT
    T.nro_telefono,
    T.nro_cliente
FROM
    E01_CLIENTE C
JOIN
    E01_TELEFONO T ON C.nro_cliente = T.nro_cliente
WHERE
    C.nombre = 'Wanda' AND
    C.apellido = 'Baker';

-- 2
SELECT DISTINCT
    C.*
FROM
    E01_CLIENTE C
JOIN
    E01_FACTURA F ON C.nro_cliente = F.nro_cliente;

-- 3
SELECT *
FROM E01_CLIENTE C
WHERE NOT EXISTS (
    SELECT 1
    FROM E01_FACTURA F
    WHERE C.nro_cliente = F.nro_cliente
);

-- 4
SELECT DISTINCT P.*
FROM E01_PRODUCTO P
JOIN E01_DETALLE_FACTURA DF ON P.codigo_producto = DF.codigo_producto;

-- 5
SELECT C.*, T.*
FROM E01_CLIENTE C
LEFT JOIN E01_TELEFONO T ON C.nro_cliente = T.nro_cliente;

-- 6
SELECT C.*, COUNT(F.nro_factura) AS cantidad_facturas
FROM E01_CLIENTE C
LEFT JOIN E01_FACTURA F ON C.nro_cliente = F.nro_cliente
GROUP BY C.nro_cliente;

-- 7
SELECT F.*
FROM E01_FACTURA F
JOIN E01_CLIENTE C ON F.nro_cliente = C.nro_cliente
WHERE C.nombre = 'Pandora' AND C.apellido = 'Tate';

-- 8
SELECT DISTINCT F.*
FROM E01_FACTURA F
JOIN E01_DETALLE_FACTURA DF ON F.nro_factura = DF.nro_factura
JOIN E01_PRODUCTO P ON DF.codigo_producto = P.codigo_producto
WHERE P.marca = 'In Faucibus Inc.';

-- 9
SELECT C.*, T.*
FROM E01_CLIENTE C
LEFT JOIN E01_TELEFONO T ON C.nro_cliente = T.nro_cliente;

-- 10
SELECT C.nombre, C.apellido, SUM(F.total_con_iva) AS gasto_total
FROM E01_CLIENTE C
LEFT JOIN E01_FACTURA F ON C.nro_cliente = F.nro_cliente
GROUP BY C.nombre, C.apellido;
