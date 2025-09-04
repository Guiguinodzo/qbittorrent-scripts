#!/bin/bash

IMAGE_TAG="/usr/local/bin/docker"

docker build . -t "$IMAGE_TAG"

echo "Uploading..."
docker image save "$IMAGE_TAG" | ssh kupakeepnas sudo /usr/local/bin/docker image load
