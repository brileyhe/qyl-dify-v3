#!/bin/bash
#
# Build the latest version of the API image
#

# Unset the KUBECONFIG
unset KUBECONFIG

# Build the image
echo "1=> Building Docker Image:"
cd .. && docker buildx build -f ./Dockerfile -t racio-api-amd64:latest --platform=linux/amd64/v3 -o type=docker .

# Tag the image
echo "2=> Tag Docker Image:"
docker tag racio-api-amd64:latest tencent/racio-api:3.9.1-$(date +%y%m%d)

# List the image
echo "3=> Listing all Docker images:"
docker images | grep racio-api