#!/bin/bash
# This script creates a Docker container for the average user.
# The user selects an input directory and an output directory the container
# can use as volumes.
#
# The input directory is where the images go
#
# The output directory is where the output .ps files go.
#
# Usage: ./launch.sh [input_dir [output_dir]]
# input_dir defaults to input/
# output_dir defaults to output/
# IMPORTANT: Both paths must be absolute, otherwise Docker will complain :(
INPUT_DIR=${1:-$(pwd)/input/}
OUTPUT_DIR=${2:-$(pwd)/output/}

docker run \
  -v $INPUT_DIR:/app/input \
  -v $OUTPUT_DIR:/app/output \
  -it ptrgags/color-by-numbers:latest
