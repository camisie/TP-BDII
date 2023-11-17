SELECT DISTINCT
    C.*
FROM
    E01_CLIENTE C
JOIN
    E01_FACTURA F ON C.nro_cliente = F.nro_cliente;

