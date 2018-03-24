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

## How it Works

### Downscale Algorithm

This algorithm does the following:

1. Read the command line arguments. (see `./main.py downscale --help`)
1. Read in the input image and convert it to grayscale.
1. We want to subdivide the image into a grid of squares. Using the image size,
    the page size (`--page-size`), the margin size (`--margin`), and the
    desired size per square(`--square-size`), calculate how many pixels wide
    each grid square is on the input image.
1. Shrink the image, converting squares of the calculated size into single
    pixels. The average color is taken for each square.
1. Bucket the colors of this downsampled image into the number specified
    by the user (`--num-colors`).
1. Scale down these values from `[0, 255]` to `[0, num_colors)`.
1. Use Jinja2 to template a PostScript file that draws a grid with a number
    per cell. These numbers correspond to the numbers we assigned in the
    previous step.
1. Write the PostScript file to the output directory.

[Here is an example I colored](https://ptrgags.deviantart.com/art/2018-03-21-WIP-Sample-Color-By-Numbers-736609991)

### Shapes Algorithm

This algorithm does the following:

1. Read the command line arguments
1. Read in the image and convert it to grayscale
1. Given the page size (`--page-size`), margin size (`--margin`) and the size
    of the image, calculate how many points of the output file are needed per
    pixel of the input image.
1. Now let's start covering the page with shapes! Repeat the following for
    every iteration from 0 to `--iterations`:
    1. Compute the diameter of the circles for this iteration. Start with
        about half the print area's (page - margins) shorter side. Then do
        1/4, 1/8, etc., halving the diameter at each iteration.
    1. Calculate how many shapes we need to approximately cover the print
        area. I use the formula `img.rows * img.cols / circle_diameter ** 2`
        I'm using the bounding box rather than the circle itself, it's close
        enough.
    1. Randomly pick the shape types. Circles and regular polygons from 3-8
        sides are all equally likely. Note that even the polygons will be
        colored from a circular region of the input image. The result of this
        is an array of PostScript commands for the different shapes.
    1. Calculate the colors for each shape. This involves the following:
        1. Randomly select a slice out of the image of size
            `circle_diameter x circle_diameter`. Keep track of the positions of
            these slices in the image.
        1. Compute the average color using a circularly-shaped kernel of the
            same size as the circle.
        1. Quantize the colors so there are only `--num-colors` values
        1. Assign each value a color. `0` is always assigned black. `1` is
            always assigned red. all the other `--num-colors - 2` colors have
            evenly spaced hues around the color wheel
    1. Calculate the centers and radii of the circles *in points* so we
        know where and how big the shapes are in PostScript
    1. Generate lines of PostScript code that look like this:
        `hue saturation brightness x y r shape_command`
1. Finally, gather up the lines of PostScript code and use Jinja2 to insert
    them into a PostScript template.
