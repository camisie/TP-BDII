SELECT
    T.nro_telefono,
    T.nro_cliente
FROM E01_CLIENTE C
JOIN E01_TELEFONO T ON C.nro_cliente = T.nro_cliente
WHERE C.nombre = 'Wanda' AND C.apellido = 'Baker';


