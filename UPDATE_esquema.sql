-- CLIENTE
BEGIN;

CREATE SEQUENCE e01_cliente_nro_cliente_seq OWNED BY E01_CLIENTE.nro_cliente;

SELECT
  SETVAL (
    'e01_cliente_nro_cliente_seq',
    (
      SELECT
        MAX(nro_cliente) + 1 AS max
      FROM
        public.E01_CLIENTE
    ),
    false
  );

ALTER TABLE E01_CLIENTE
ALTER COLUMN nro_cliente
SET DEFAULT nextval ('e01_cliente_nro_cliente_seq');

COMMIT;

-- TELEFONO
BEGIN;

ALTER TABLE E01_TELEFONO
DROP CONSTRAINT fk_e01_telefono_cliente,
ADD CONSTRAINT fk_e01_telefono_cliente FOREIGN KEY (nro_cliente) REFERENCES E01_CLIENTE (nro_cliente) ON DELETE CASCADE;

COMMIT;

-- PRODUCTO
BEGIN;

CREATE SEQUENCE e01_producto_codigo_producto_seq OWNED BY E01_PRODUCTO.codigo_producto;

SELECT
  SETVAL (
    'e01_producto_codigo_producto_seq',
    (
      SELECT
        MAX(codigo_producto) + 1 AS max
      FROM
        public.E01_PRODUCTO
    ),
    false
  );

ALTER TABLE E01_PRODUCTO
ALTER COLUMN codigo_producto
SET DEFAULT nextval ('e01_producto_codigo_producto_seq');

COMMIT;
