#!/bin/bash
#
# Name: startup.sh
# Author: Kenson Man <kenson@breakthrough.org.hk>
# Desc:   The startup script to startup the docker container
#

#Container Name
CNAME=imcwc
#Image Name
INAME=imcwc
#DBContainer Version/Image
DVERSION=9
#DBUsername
USERNAME=imcwc
GID="$(id -g)"

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
	docker build --build-arg UID=${UID} --build-arg GID=${GID} --build-arg USERNAME=${USERNAME} -t ${INAME} .
fi

docker run --rm --name ${CNAME} -p 8000:8000 -v "$(pwd)":/usr/src/app -it ${INAME} $@
