#! /bin/bash
set -x

if [[ ! -f manage.py ]]; then
    echo "No manage.py, wrong location"
    exit 1
fi

sleep 2
docker rm -f fnet-mysql-dev
docker run -it -d -e MYSQL_DATABASE=fnet -e MYSQL_USER=fnet -e MYSQL_PASSWORD=fnet -e MYSQL_ROOT_PASSWORD=root -p 127.0.0.1:3306:3306 --name fnet-mysql-dev mysql:8.0.27

if [ "$1" = "--migrate" ]; then
    sleep 3
    echo `cat /dev/urandom | head -1 | md5sum | head -c 32` > data/config/secret.key
    python manage.py migrate
fi