#!/bin/bash

# Bring up all services
./scripts/run.sh

# Build frontend test image
docker build -t setu-frontend-test ./setu-frontend -f ./setu-frontend/Dockerfile.test --no-cache

# Run the frontend test image in a container(run the frontent tests)
docker run --rm --name setu-frontend-test setu-frontend-test

# Bring down all services
./scripts/down.sh
