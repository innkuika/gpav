#!/bin/bash

# example usage: ENV=prod mange.sh runserver

if [ $ENV == "prod" ]
then
  cp .env.prod .env
  python manage.py "${@:1}"
elif [ $ENV == "dev" ]
then
  cp .env.dev .env
  python manage.py "${@:1}"
fi
