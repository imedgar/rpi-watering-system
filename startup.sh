#!/bin/sh

APP_NAME=
HOST=
PORT=

. ./server.config

gunicorn ${APP_NAME}:app -p ${APP_NAME}.pid -b ${HOST}:${PORT} -D
echo "Gunicorn started at ('${HOST}', '${PORT}')"