#!/bin/sh

APP=/app
DATA=/data

mkdir -p $DATA/log $DATA/config

if [ ! -f "$DATA/config/secret.key" ]; then
    echo $(cat /dev/urandom | head -1 | md5sum | head -c 32) > "$DATA/config/secret.key"
fi

cd $APP

n=0
while [ $n -lt 2 ]
do
    python manage.py migrate --no-input &&
    echo "from django.contrib.auth.models import User; User.objects.create_superuser('root', 'rootroot')" | python manage.py shell && 
    break
    n=$(($n+1))
    echo "Failed to migrate, going to retry..."
    sleep 3
done

exec supervisord -c /app/deploy/supervisord.conf