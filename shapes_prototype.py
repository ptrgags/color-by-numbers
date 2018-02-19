#!/usr/bin/env python
"""
This is a prototype of a separate color-by-numbers script that generates
overlapping shapes.
"""
import cv2
import numpy

def circle_mask(image, center, r):
    """
    Make a Numpy mask for an image in the shape of a circle.
    """
    # unpack parameters
    cx, cy = center
    w, h = image.shape

    # Caclulate a boolean array that is True when inside a circle
    ys, xs = numpy.mgrid[:w, :h]
    return (xs - cx) ** 2 + (ys - cy) **  2 <= r ** 2

def main():
    img = cv2.imread('images/keys.jpg')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Use a circle mask to select a portion of the image
    mask = circle_mask(gray, (200, 440), 200)
    result = numpy.zeros(gray.shape)
    result[mask] = gray[mask].mean()
    result[~mask] = 255
    cv2.imwrite('output/circle.png', result)

if __name__ == '__main__':
    main()
