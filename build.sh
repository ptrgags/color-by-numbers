#!/bin/bash
# This script builds the official build of Color by Numbers
VERSION=$(cat VERSION)

# Make the build and tag it with a version number
docker build \
-t ptrgags/color-by-numbers:latest \
-t ptrgags/color-by-numbers:$VERSION .
