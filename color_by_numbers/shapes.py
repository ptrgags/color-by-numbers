"""
Shapes takes an image and generates a pattern of overlapping
polygons

Each polygon has a color number like in downscale. However, since
putting labels on each region would be confusing to look at,
I changed it so that each polygon is stroked with a different color.
"""
import itertools

import cv2
import numpy
from jinja2 import Environment, PackageLoader

from color_by_numbers.page_size import DimensionsCalculator

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

def pick_shapes(num_samples):
    """
    Randomly pick shapes. These correspond to
    PostScript commands in the jinja template.

    Supported shapes:
    '3 poly'
    ...
    '8 poly'
    'circle'
    """
    MIN_SIDES = 3
    MAX_SIDES = 8
    poly_shapes = [f'{n} poly' for n in range(MIN_SIDES, MAX_SIDES + 1)]
    all_shapes = poly_shapes + ['circle']
    return numpy.random.choice(all_shapes, num_samples)

def make_circle_mask(diameter):
    """
    Make a circle-shaped mask in a rectangle of size diameter x diameter.

    This mask will be used like a kernel that does an average blur within
    a circle. Anything outside the circle will not be included in the sum.
    """

    # Generate an empty mask diameter x diameter
    mask = numpy.zeros((diameter, diameter))

    # Generate centered x and y coordinates
    ys, xs = numpy.mgrid[:diameter, :diameter]
    radius = diameter // 2
    centered_ys = ys - radius
    centered_xs = xs - radius

    # Paint a circle with radius `radius`
    circle = centered_xs ** 2 + centered_ys ** 2 <= radius ** 2
    mask[circle] = 1

    # Normalize the mask by dividing by the total number of cells with
    # a 1 in them:
    mask /= mask.sum()

    return mask

def pick_mask_offsets(img, diameter, num_samples):
    """
    Randomly slide the mask to a position (row, col) so it fits within the
    size of the image
    """
    # randomly pick rows and columns. The kernel must stay within the bounds
    # of the image because I said so.
    rows, cols = img.shape
    row_offsets = numpy.random.randint(rows - diameter + 1, size=num_samples)
    col_offsets = numpy.random.randint(cols - diameter + 1, size=num_samples)

    # Turn the offsets into two columns of a larger matrix. This way we can
    # think of it as N 2-vectors (row, col)
    return numpy.stack([row_offsets, col_offsets], axis=1)

def make_slice(offset, diameter, img):
    """
    make a slice from the image.
    """
    row, col = offset
    return img[row:row + diameter, col:col + diameter]

def slice_image(img, mask_offsets, diameter):
    """
    Return an array of slices of an image given the row/column offsets
    """
    return numpy.apply_along_axis(make_slice, 1, mask_offsets, diameter, img)

def reduce_colors(colors, num_colors):
    """
    Quantize colors so there are only a few.
    """
    return colors // (256 // num_colors)


def calculate_colors(num_samples, diameter, img, args):
    """
    Calculate colors for all the shapes for this diameter.
    Use Numpy vector operations whenever possible.

    This returns the average colors and the mask offsets that generated them.
    """
    rows, cols = img.shape
    circle_mask = make_circle_mask(diameter)
    mask_offsets = pick_mask_offsets(img, diameter, num_samples)
    slices = slice_image(img, mask_offsets, diameter)
    avg_colors = numpy.mean(slices, axis=(1, 2))
    quantized = reduce_colors(avg_colors, args.num_colors)

    return quantized, mask_offsets

def calculate_shape_dimensions(diameter, mask_offsets, scaling_factor):
    radius_px = diameter // 2

    # mask_offsets are the top left corner. We want the center of each mask.
    centers_px = mask_offsets + radius_px

    # Convert  to points
    radius_pt = radius_px * scaling_factor
    centers_pt = centers_px * scaling_factor

    return radius_pt, centers_pt

COLORS = [
    "0.7 0.7 0.7",
    "1 0.7 0.7",
    "0.7 1 0.7",
    "0.7 0.7 1",
    "0.7 1 1",
    "0.5 0.7 1",
]

def format_postscript(colors, radius, centers, shape_commands):
    """
    Format postscript commands from the given circle geometry
    """
    num_samples =  len(colors)
    for i in range(num_samples):
        color_index = colors[i]
        # TODO: Generate this using HSB
        color = COLORS[int(color_index)]
        y, x = centers[i]
        cmd = shape_commands[i]
        yield f'{color} {x:.2f} {y:.2f} {radius} {cmd}'

def write_postcript(image_commands, args, page_size):
    """
    Write a PostScript file with the given commands
    """
    env = Environment(
        loader=PackageLoader('color_by_numbers', 'templates'))
    template = env.get_template('shapes.ps')

    w, h = page_size
    code = template.render(
        margin_size=args.margin,
        image=itertools.chain(*image_commands),
        page_width=w,
        page_height=h)

    with open(args.output, 'w') as f:
        f.write(code + '\n')

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

    # This calculator will be used to handle scaling things to
    # points
    calc = DimensionsCalculator.get_size_calculator(
        img.shape, args.paper_size, args.margin)
    scaling_factor = calc.points_per_pixel(img)

    ps_code = []

    for diameter in choose_diameters(img, args):
        print('-' * 50)

        # TODO:  Stopping condition on tiny diameters
        print('Diameter:', diameter)

        num_samples = pick_num_samples(diameter, img)
        print('Samples:', num_samples)

        shape_commands = pick_shapes(num_samples)
        print('Shape commands:', shape_commands.shape)

        colors, offsets = calculate_colors(num_samples, diameter, img, args)
        print('Colors:', colors.shape)
        print('Offsets:', offsets.shape)

        # get the radius (scalar) and the coordinates of the center
        # in points
        radius, centers = calculate_shape_dimensions(
            diameter, offsets, scaling_factor)

        gen = format_postscript(colors, radius, centers, shape_commands)
        ps_code.append(gen)

    write_postcript(ps_code, args, calc.postscript_dims)
