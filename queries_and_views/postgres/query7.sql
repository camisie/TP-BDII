SELECT F.*
FROM E01_FACTURA F
JOIN E01_CLIENTE C ON F.nro_cliente = C.nro_cliente
WHERE C.nombre = 'Pandora' AND C.apellido = 'Tate';

