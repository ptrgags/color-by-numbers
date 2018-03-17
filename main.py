#!/usr/bin/env python
import argparse

from color_by_numbers import downscale, shapes
from color_by_numbers.argparse_helpers import (
    input_image, output_postscript, paper_dimensions, to_points
)

def parse_args():
    """
    Set up a parser and parse command line arguments
    """
    # This is the main parser
    parser = argparse.ArgumentParser()

    # Every subcommand has arguments like input image and output postscript
    # file.
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument(
        'input',
        type=input_image,
        help='The input image to process. This path must begin with input/')
    common.add_argument(
        'output',
        type=output_postscript,
        help='The output file This path must match output/*.ps')
    common.add_argument(
        '-d',
        '--debug',
        action='store_true',
        help='If this flag is specified, save extra images for debugging')
    common.add_argument(
        '-p',
        '--paper-size',
        type=paper_dimensions,
        default=paper_dimensions('letter'),
        help='Choose the size of the paper')
    common.add_argument(
        '-n',
        '--num-colors',
        type=int,
        default=6,
        help='This determines how many numbers are used in the printout')
    common.add_argument(
        '-m',
        '--margin',
        type=to_points,
        default=to_points('1 in'),
        help='specify the margin size. "X in" "X cm" and "X pt" are supported')

    # Each subcommand will configure its own subparser
    subparsers = parser.add_subparsers(dest='sub_command')
    subparsers.required = True
    downscale.configure_parser(subparsers, common)
    shapes.configure_parser(subparsers, common)

    return parser.parse_args()

def main():
    """
    Entry point for the program
    """
    args = parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
