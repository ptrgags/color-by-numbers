#!/usr/bin/env python
"""
This is a prototype of my color-by-numbers script. I still need to plan this
out more.
"""
import cv2
import numpy

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

def get_numbers(image, num_colors=8):
    """
    Convert from a range of [0, 256)
    to a range [0, num_colors). This will
    be the grey values used in the color by numbers.
    """
    # How  many steps are per color?
    N = 256 // num_colors

    # Divide to get which grey value to display
    return image // N


def to_ascii(image):
    """
    Take an image with 8 or less colors and
    convert it to an ascii representation
    """
    # Make a lookup table of the ascii characters
    # to represent the image
    gradient = '@#*+-:. '
    table = numpy.array(list(gradient))

    # Use Numpy's fancy indexing to look up all the
    # characters at once
    return table[image]

def main():
    """
    Main Script
    """
    # Read in an image
    img = cv2.imread('images/gears.jpg')

    # Make it grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Output the grayscale image
    cv2.imwrite('output/gray.png', gray)

    # Downsample the grayscale image
    small = downsample(gray)
    cv2.imwrite('output/downsampled.png', small)

    # Reduce the color depth
    numbers = get_numbers(small)
    cv2.imwrite('output/reduced.png', numbers * (256 // 8))

    # Convert to ascii!
    text = to_ascii(numbers)

    # Print the result!
    for row in text:
        print(''.join(row))

if __name__ == '__main__':
    main()
