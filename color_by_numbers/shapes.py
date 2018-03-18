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

def pick_shapes(num_samples):
    """
    Randomly pick shapes. These correspond to
    PostScript commands in the jinja template.

    Supported shapes:
    '3 poly'
    ...
    '8 poly'
    'square'
    'circle'
    """
    MIN_SIDES = 3
    MAX_SIDES = 8
    poly_shapes = [f'{n} poly' for n in range(MIN_SIDES, MAX_SIDES + 1)]
    all_shapes = poly_shapes + ['square', 'circle']
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

    #scaling_factor = calculate_points_per_pixel(img, args)

    for diameter in choose_diameters(img, args):
        print('-' * 50)

        # TODO:  Stopping condition on tiny diameters
        print('Diameter:', diameter)

        num_samples = pick_num_samples(diameter, img)
        print('Samples:', num_samples)

        shape_commands = pick_shapes(num_samples)
        print('Shape commands:', shape_commands.shape)

        #radius = calculate_radius(diameter, img)
        colors, offsets = calculate_colors(num_samples, diameter, img, args)
        print('Colors:', colors.shape)
        print('Offsets:', offsets.shape)

        # TODO: calculate radii and shape centers in points
        #radius, centers = calculate_shape_dimensions(
        #    diameter, centers, scaling_factor)
