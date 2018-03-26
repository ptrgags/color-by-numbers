"""
Downscale is the simplest form of turning an image into a color-by-numbers page.
It downsamples the image and computes the average color in each block.
"""
import cv2
import numpy
from jinja2 import Environment, PackageLoader

from color_by_numbers.common import debug_save
from color_by_numbers.argparse_helpers import to_points
from color_by_numbers.page_size import DimensionsCalculator

def downsample(image, block_size):
    """
    Take a grayscale image and downsample. Downsampling is done
    by averaging blocks of block_size x block_size
    """
    # unpack the size of the input image
    in_rows, in_cols = image.shape

    # Make a buffer for the output image
    out_rows = in_rows // block_size
    out_cols = in_cols // block_size
    result = numpy.zeros((out_rows, out_cols), numpy.uint8)

    # Iterate over the output image
    for i in range(out_rows):
        for j in range(out_cols):
            # Scale to pixels of input image
            row = i * block_size
            col = j * block_size

            # Slice out a rectangle from the input image
            img_slice = image[row:row + block_size, col: col + block_size]

            # Set the output pixel to the average of the block
            result[i, j] = img_slice.mean()

    # Return the new tiny image
    return result

def assign_numbers(image, num_colors):
    """
    Convert from a range of [0, 256)
    to a range [0, num_colors). This will
    be the grey values used in the color by numbers.
    """
    # How  many steps are per color?
    bucket_size = 256 / num_colors

    # Divide to get which grey value to display
    return (image // bucket_size).astype(int)

def format_postscript(image, args, page_size):
    """
    Take an image and format it as a PostScript file. Most of the code
    is in a Jinja2 template.
    """
    env = Environment(
        loader=PackageLoader('color_by_numbers', 'templates'))
    template = env.get_template('downscale.ps')

    w, h = page_size
    return template.render(
        square_size=args.square_size,
        margin_size=args.margin,
        # flip the image since PostScript has a y-up coordinate system.
        image=reversed(image),
        page_width=w,
        page_height=h)

def configure_parser(subparsers, common):
    """
    Configure parser for the downscale subcommand
    """
    parser_ds = subparsers.add_parser('downscale', parents=[common])
    parser_ds.add_argument(
        '-s',
        '--square-size',
        type=to_points,
        default=to_points('0.25 in'),
        help="Size of each square in the grid")
    parser_ds.set_defaults(func=main)

def main(args):
    """Entry point for the downscale script"""

    print("Generating a color-by-numbers page with the Downscale algorithm!")
    print(f'Image size (rows, cols): {args.input.shape}')
    print(f'Paper size (pt.): {args.paper_size}')
    print(f'Margins (pt.): {args.margin}')

    # Make the input image grayscale
    print("Converting to grayscale...")
    img = cv2.cvtColor(args.input, cv2.COLOR_BGR2GRAY)
    debug_save('gray.png', img, args)

    # This calculator handles differences in portrait/landscape orientation.
    # Let's use it to calculate the block size in pixels/block
    calc = DimensionsCalculator.get_size_calculator(
        img.shape, args.paper_size, args.margin)
    block_size = calc.block_size(img.shape, args.square_size)
    print(f'Calculated block size (px/block): {block_size}')

    # scale down the image, taking average colors per block.
    print("Downscaling...")
    img = downsample(img, block_size)
    debug_save('downsampled.png', img, args)
    print(f'Downsampled image size (px): {img.shape}')

    # Reduce the number of colors
    print("Numbering colors...")
    numbers = assign_numbers(img, args.num_colors)
    debug_save('reduced.png', numbers * (256 // args.num_colors), args)

    # Generate the PostScript file
    print("Generating printout...")
    with open(args.output, 'w') as f:
        ps_code = format_postscript(numbers, args, calc.postscript_dims)
        f.write(ps_code + '\n')
    print("Done!")
