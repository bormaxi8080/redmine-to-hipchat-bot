#!/bin/bash

if [ -n "${DEV_UID}" ]; then
    usermod -u ${DEV_UID} www-data
fi
if [ -n "${DEV_GID}" ]; then
    groupmod -g ${DEV_GID} www-data
fi
python /var/www/main.py

tail -f /dev/null