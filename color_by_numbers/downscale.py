"""
Downscale is the simplest form of turning an image into a color-by-numbers page.
It downsamples the image and computes the average color in each block.
"""
import cv2
import numpy

from color_by_numbers.common import debug_save
from color_by_numbers.argparse_helpers import to_points
from color_by_numbers.page_size import DimensionsCalculator

def downsample(image, block_size=32):
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
