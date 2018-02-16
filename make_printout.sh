#!/bin/bash
python color_by_numbers.py > output/fragment.ps
cat template.ps output/fragment.ps > output/sample.ps
