#!/bin/bash

CONTAINER_NAME='lambdapack'
# Checking if docker container with $CONTAINER_NAME name exists.
CID=$(docker ps -a -q -f name=^/${CONTAINER_NAME}$)
if [ "${CID}" ]; then
     docker stop $CONTAINER_NAME
     docker rm $CONTAINER_NAME
fi
unset CID

docker run -d -t --name $CONTAINER_NAME -v $(pwd):/host amazonlinux:latest
docker exec -i -t $CONTAINER_NAME bash /host/build_pack_script.sh
