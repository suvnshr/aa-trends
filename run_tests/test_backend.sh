#!/bin/bash

# Bring up all services
./scripts/run.sh

# Build backend test image
docker build -t setu-backend-test ./setu-backend -f ./setu-backend/Dockerfile.test --no-cache

# Run the backend test image in a container(run the backend tests)
docker run --env-file=./setu-backend/.env --rm --network=host  --name setu-backend-test setu-backend-test

# Bring down all services
./scripts/down.sh
