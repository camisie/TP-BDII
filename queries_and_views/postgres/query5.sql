SELECT C.*, T.*
FROM E01_CLIENTE C
LEFT JOIN E01_TELEFONO T ON C.nro_cliente = T.nro_cliente;


