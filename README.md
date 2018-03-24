# Color by Numbers (2018)

This is a Python script that uses OpenCV and Jinja2 to turn photos into
coloring book pages!

This is also an exercise for me to learn about Docker. This script is designed
to run in a Docker container. Two directories are mounted so the images and
output are stored on the host, not in the container.

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
    There are many options to `main.py`, keep reading to learn more!
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
