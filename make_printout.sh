#!/bin/bash
python color_by_numbers.py > output/downscale_example.ps
ps2pdf output/downscale_example.ps output/downscale_example.pdf
