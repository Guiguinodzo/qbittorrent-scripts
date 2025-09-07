#!/bin/bash

IMAGE_TAG="qbittorrent-cron:latest"

echo "Uploading..."
docker image save "$IMAGE_TAG" | ssh kupakeepnas sudo /usr/local/bin/docker image load
