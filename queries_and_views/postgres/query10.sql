SELECT C.nombre, C.apellido, SUM(F.total_con_iva) AS gasto_total
FROM E01_CLIENTE C
LEFT JOIN E01_FACTURA F ON C.nro_cliente = F.nro_cliente
GROUP BY C.nombre, C.apellido;
