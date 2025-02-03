#!/bin/bash
echo "Deploying the Python DevSecOps App..."
docker stop my-app || true
docker rm my-app || true
docker pull my-docker-repo/my-python-app:latest
docker run -d -p 5001:5000 --name my-app my-docker-repo/my-python-app:latest
echo "Deployment completed!"
