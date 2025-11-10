#!/bin/bash
set -e

# Leer contraseña desde archivo si existe
if [ -v PASSWORD_FILE ]; then
    PASSWORD="$(< $PASSWORD_FILE)"
fi

# Configuración de base de datos (variables de entorno o valores por defecto)
DB_HOST=${DB_HOST:-${DB_PORT_5432_TCP_ADDR:-db}}
DB_PORT=${DB_PORT:-${DB_PORT_5432_TCP_PORT:-5432}}
DB_USER=${DB_USER:-${DB_ENV_POSTGRES_USER:-${POSTGRES_USER:-odoo}}}
DB_PASSWORD=${DB_PASSWORD:-${DB_ENV_POSTGRES_PASSWORD:-${POSTGRES_PASSWORD:-odoo}}}

# Construir argumentos para wait-for-psql.py
DB_ARGS=(--db_host "$DB_HOST" --db_port "$DB_PORT" --db_user "$DB_USER" --db_password "$DB_PASSWORD")

# Esperar a que la base de datos esté disponible
wait-for-psql.py "${DB_ARGS[@]}" --timeout=30

# Lanzar Odoo con debugpy si DEBUGPY está activado
if [ -n "$DEBUGPY" ]; then
    echo "Iniciando Odoo con debugpy en el puerto $DEBUGPY_PORT..."
    exec python3 -Xfrozen_modules=off -m debugpy \
        --listen 0.0.0.0:$DEBUGPY_PORT \
        /usr/bin/odoo -c /etc/odoo/odoo.conf "${DB_ARGS[@]}"
else
    echo "Iniciando Odoo normalmente..."
    exec /usr/bin/odoo -c /etc/odoo/odoo.conf "${DB_ARGS[@]}"
fi
