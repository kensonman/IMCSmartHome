#!/bin/bash
#
# Name: startup.sh
# Author: Kenson Man <kenson@breakthrough.org.hk>
# Desc:   The startup script to startup the docker container
#

#Container Name
CNAME=imcgw
#Image Name
INAME=imcgw
#DBContainer Version/Image
DVERSION=9
#DBUsername
USERNAME=imcgw
GID="$(id -g)"
PORT=9807

RST="$(docker ps | grep $CNAME)"
if [ ! -z "$RST" ]; then
	echo "Stopping the last container..."
	docker stop "${CNAME}"
fi

RST="$(docker ps -a | grep $CNAME)"
if [ ! -z "$RST" ]; then
	echo "Removing the last container..."
	docker rm "${CNAME}"
fi

RST="$(docker images -a | grep $INAME)"
if [ -z "$RST" ]; then
	echo "Creating the container images..."
	docker build --build-arg UID=${UID} --build-arg GID=${GID} --build-arg USERNAME=${USERNAME} --build-arg PORT=${PORT} -t ${INAME} .
fi

docker run --rm --name ${CNAME} -p ${PORT}:${PORT} -v "$(pwd)":/usr/src/app -it ${INAME} $@
