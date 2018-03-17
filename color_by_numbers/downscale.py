"""
Downscale is the simplest form of turning an image into a color-by-numbers page.
It downsamples the image and computes the average color in each block.
"""
import cv2

from color_by_numbers.common import debug_save

def configure_parser(subparsers, common):
    """
    Configure parser for the downscale subcommand
    """
    parser_ds = subparsers.add_parser('downscale', parents=[common])
    parser_ds.set_defaults(func=main)

def main(args):
    """Entry point for the downscale script"""

    # Make the input image grayscale
    img = cv2.cvtColor(args.input, cv2.COLOR_BGR2GRAY)
    debug_save('gray.png', img, args)
