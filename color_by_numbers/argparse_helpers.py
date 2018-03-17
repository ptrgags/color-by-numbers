"""
This file contains Argparse type functions for use in subcommands.
"""
import cv2
import argparse

def input_image(fname):
    """
    Validate that a filename matches 'input/*'. Open it as
    an image.
    """
    if not fname.startswith('input/'):
        raise argparse.ArgumentTypeError('input file must be in input/')

    # Read an image from the input directory
    img = cv2.imread(fname)

    # make sure we got an image
    if img is None:
        raise argparse.ArgumentTypeError('{} not found'.format(fname))

    return img

def output_postscript(fname):
    """
    validate that a filename matches 'output/*.ps'. Do not open the file
    for writing, this will be handled by the commmand.
    """
    if not fname.startswith('output/'):
        raise argparse.ArgumentTypeError('output filename must be in output/')
    if not fname.endswith('.ps'):
        raise argparse.ArgumentTypeError('output filename must end in .ps')

    return fname
