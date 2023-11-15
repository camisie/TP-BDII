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
