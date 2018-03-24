# Color by Numbers (2018)

This is a Python script that uses OpenCV and Jinja2 to turn photos into
coloring book pages!

## Overview

This Python script currently has 2 algorithms for generating coloring printouts:

1. "Downscale" - This algorithm shrinks the image to a really low resolution.
    it then draws a numbered grid on a page that describes the brightness
    of each pixel.
2. "Shapes" - This algorithm overlaps a bunch of circles and regular polygons on
    a page. Each shape is assigned a brightness value after sampling pixels from
    the input image.

Output is always in PostScript format. These files can be converted to
PDF format by programs such as GhostScript's `ps2pdf` if needed.

## Purpose

This is just a fun little Python project I made to turn photos into coloring
pages. The idea for this project came from a coloring book series,
[Querkles](http://www.querkles.net/) by Thomas Pavitte. Be sure to check out
his coloring books if you like this project!

This is also an exercise for me to learn about Docker. This script is designed
to run in a Docker container. Two directories are mounted so the images and
output are stored on the host, not in the container.

This is also an exercise in learning the PostScript programming language. It's
a language used by printers to lay out a page of text and vector graphics.

## Quickstart (Docker)

This assumes you already have Docker installed.

1. Clone this Git repo.
1. Run `launch.sh`. This script does the following:
    1. Pull the latest Docker container for `color-by-numbers` from Docker Hub
    1. Mount the `input/` and `output/` directories of this Git repo.
    1. Start Bash within the container. Now we are ready to process some
        images!
1. (Optional) Put an image into the `input/` directory **on the host machine**.
    You can ignore this step if you want to use one of the sample images
    provided in the repo.
1. Run the python script **inside the Docker container**. Some examples:
    ```
    ./main.py downscale input/gears.jpg output/gears_downscale.ps
    ./main.py shapes input/gears.jpg output/gears_shapes.ps
    ```
    There are many options to `main.py`, use the `-h` flag to learn more!
1. (Optional) Convert the PostScript output to a PDF file. GhostScript is
    already installed in the container, so simply run a command like this
    **inside the Docker container**:
    ```
    # from /app inside the container
    ps2pdf output/gears_downscale.ps output/gears_downscale.pdf

    # it's a lot simpler if we enter the output folder:
    cd output
    #  this creates gears_downscale.pdf automatically
    ps2pdf gears_downscale.ps
    ```

## Running Without Docker

This script is really designed for use inside Docker. However, if you want to
run the Python code from the repo directly, follow these instructions.

**Note**: I have not tested this myself.

### Installing Dependencies

* Install Python modules with the usual `pip install -r requirements.txt`
* If you want to be able to convert PostScript -> PDFs, install GhostScript

### Caveats of Running Outside Docker

* Input images **MUST** go in the `input/` directory of this repo. The Python
  script assumes that there will be directories called `input/` and `output/`
  in the same directory as `main.py`. In the Docker container, those two
  two directories are created by mounting 2 directories on the host machine.
* The output directory **MUST** be the `output/` directory of this repo for the
  same reasons.
