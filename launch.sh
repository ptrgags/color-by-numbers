#!/bin/bash

# This uses a local image I made from the Dockerfile
docker run -v $(pwd):/app -it ptrgags/color-by-numbers:dev
