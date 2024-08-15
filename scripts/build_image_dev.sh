#!/bin/bash
set -e
set -o pipefail

source source_env.sh

echo ${DOCKER_REGISTRY_URL}/lawrag-devcontainers

# docker build --rm=false -t lawrag-devcontainers -t ${DOCKER_REGISTRY_URL}/lawrag-devcontainers -f Dockerfile.dev .
docker build --rm=false -t lawrag-devcontainers -t hisiter/lawrag-devcontainers -f Dockerfile.dev .
docker push hisiter/lawrag-devcontainers