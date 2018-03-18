"""
Shapes takes an image and generates a pattern of overlapping
polygons

Each polygon has a color number like in downscale. However, since
putting labels on each region would be confusing to look at,
I changed it so that each polygon is stroked with a different color.
"""
import numpy
import cv2

def choose_diameters(img, args):
    """
    Generate a sequence of diameters for the shapes
    based on the image size.
    """
    # find the shorter side length of the image
    rows, cols = img.shape
    short_dim = min(rows, cols)

    # Start with circles with diameters of 1/2 the
    # shorter side of the image.
    # Then do 1/4 the image.
    # Then 1/8. Etc.
    divisors = [2 ** i for i in range(1, args.iterations + 1)]
    for divisor in divisors:
        yield short_dim // divisor

def pick_num_samples(diameter, img):
    """
    We want to make enough samples of the image to cover
    most of the image
    """
    rows, cols = img.shape
    area = rows * cols

    # Use the bounding box area instead of the circle area. This
    # is simpler to compute and shouldn't make a big difference.
    shape_area = diameter * diameter

    return area // shape_area

def configure_parser(subparsers, common):
    """
    Configure parser for the downscale subcommand
    """
    # Downscale arguments
    parser_shapes = subparsers.add_parser('shapes', parents=[common])
    parser_shapes.add_argument(
        '-i',
        '--iterations',
        type=int,
        default=6,
        help=(
            'Maximum number of iterations of covering the image with circles. '
            'Note that this is O(n^2) in the number of iterations'))
    parser_shapes.set_defaults(func=main)

def main(args):
    """
    Entry point for the shapes method
    """
    # Convert input image to grayscale and flip upside down
    # since PostScript uses a y-up coordinate system
    img = cv2.cvtColor(args.input, cv2.COLOR_BGR2GRAY)
    img = numpy.flipud(img)

    for diameter in choose_diameters(img, args):
        # TODO:  Stopping condition on tiny diameters
        print('Diameter:', diameter)

        num_samples = pick_num_samples(diameter, img)
        print('Samples:', num_samples)

        #region_shapes = pick_shapes(num_samples)
        #radius = calculate_radius(diameter, img)
        #colors = calculate_colors(num_samples, diameter, img)
