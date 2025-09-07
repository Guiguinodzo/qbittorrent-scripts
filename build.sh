#!/bin/bash

IMAGE_TAG="qbittorrent-cron:latest"

docker build . -t "$IMAGE_TAG"
