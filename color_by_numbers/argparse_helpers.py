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

def paper_dimensions(dims):
    """
    Get the width and height of a piece of paper in portrait orientation

    Supported inputs:
    'letter' -> '8.5 in x 11 in'
    'A4' -> '210 mm x 297 mm'
    '<width> x <height>' where width and height are valid inputs to to_points()
    """
    PRESETS = {
        'letter': '8.5 in x 11 in',
        'A4': '210 mm x 297 mm'
    }
    # Lookup presets. Default to the original string.
    preprocessed = PRESETS.get(dims.lower(), dims)

    try:
        # Convert to width/height using to_points
        w, h = [to_points(x.strip()) for x in preprocessed.split(' x ')]
        return w, h
    except ValueError as e:
        raise argparse.ArgumentTypeError(
            'dimensions must be "letter", "A4" or "<width> x <height>"')

def to_points(dim):
    """
    Convert inches, mm, or cm to points.

    Formats accepted:
    N in
    N mm
    N cm
    N pt
    """
    try:
        quantity, units = dim.split(' ')
    except ValueError as e:
        raise argparse.ArgumentTypeError(
            f'dimension {dim} must be in the format "<quantity> <unit>"')

    TO_POINTS = {
        'in': 72.0,
        'cm': 28.3465,
        'mm': 2.3465,
        'pt': 1.0
    }

    try:
        # Convert to points
        scale_factor = TO_POINTS[units]
        quantity = float(quantity)
        return quantity * scale_factor
    except KeyError as e:
        valid_units = list(TO_POINTS.keys())
        raise argparse.ArgumentTypeError(
            f'{units} is not a supported unit. Use one of {valid_units}')
    except ValueError as e:
        raise argparse.ArgumentTypeError(
            f'{quantity} must be a valid float')
