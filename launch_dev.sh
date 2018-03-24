#!/bin/bash
# This script creates a Docker container for the app set up for development.
# It mounts the current directory as /app, so I can work on the code
# without rebuilding the container
docker run -v $(pwd):/app -it ptrgags/color-by-numbers:latest
