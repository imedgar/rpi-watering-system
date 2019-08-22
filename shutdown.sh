#!/bin/sh

APP_NAME=

. ./server.config

kill -HUP `cat $APP_NAME.pid`
kill `cat $APP_NAME.pid`