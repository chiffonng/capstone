#!/bin/bash

# Load environment variables from .env file
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

# Check the value of CRAWL
if [ "${CRAWL}" == "TRUE" ]; then
  echo "Starting Nutch and Solr for data crawling..."
  docker compose -f docker/docker-compose.crawl.yml up -d
else
  echo "Starting PyTorch for model training/evaluation..."
  docker build -t pytorch_cuda -f docker/Dockerfile .
fi
