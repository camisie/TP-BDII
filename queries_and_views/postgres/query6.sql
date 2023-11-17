SELECT C.*, COUNT(F.nro_factura) AS cantidad_facturas
FROM E01_CLIENTE C
LEFT JOIN E01_FACTURA F ON C.nro_cliente = F.nro_cliente
GROUP BY C.nro_cliente;

