export PGPASSWORD=$PSQL_PASSWORD

until psql -h $PSQL_HOST -p $PSQL_PORT -U postgres -d $PSQL_DB_NAME -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done
psql -h $PSQL_HOST -p $PSQL_PORT -U postgres -d $PSQL_DB_NAME -a -f ./ITBA_2023_esquema_facturacion.sql
psql -h $PSQL_HOST -p $PSQL_PORT -U postgres -d $PSQL_DB_NAME -a -f ./UPDATE_esquema.sql

echo "Data uploaded"

pip install -r ./requirements.txt
python ./migration.py
