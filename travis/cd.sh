#!/usr/bin/env bash

if [ -z "$TRAVIS_TAG" ]; then
  echo "Build is not a release, skipping CD" >&2; exit 0
fi

if [ -z "$DOCKERIO_USERNAME" -o -z "$DOCKERIO_PASSWORD" ]; then
  echo "No docker.io credentials configured, unable to publish builds" >&2; exit 1
fi

set -euo pipefail

export APP_PORT="80"
export BUILD_TAG="$TRAVIS_TAG"
touch .env

docker-compose build

docker login --username="$DOCKERIO_USERNAME" --password="$DOCKERIO_PASSWORD"

docker-compose config | grep -Po '(?<=image: ).*$' | sort -u | while read image; do
  docker push "$image"
done
