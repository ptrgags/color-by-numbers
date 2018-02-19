#!/usr/bin/env python
"""
This is a prototype of a separate color-by-numbers script that generates
overlapping shapes.
"""
import cv2
import numpy
import random
import math

def circle_mask(image, center, r):
    """
    Make a Numpy mask for an image in the shape of a circle.
    """
    # unpack parameters
    cx, cy = center
    rows, cols = image.shape

    # Caclulate a boolean array that is True when inside a circle
    ys, xs = numpy.mgrid[:rows, :cols]
    return (xs - cx) ** 2 + (ys - cy) **  2 <= r ** 2

def paint_shapes(image):
    # Start with an empty buffer the size of the image
    result = numpy.zeros(image.shape)

    # Unpack the shape of the array, we'll need it in the loop
    rows, cols = image.shape
    area = rows * cols

    # Start with big shapes and get progressively smaller
    radii = [256, 128, 64, 32, 16, 8]
    for i, radius in enumerate(radii):
        circle_area = math.pi * radius * radius
        iterations = int(area // circle_area)
        print(f"i={i}, r={radius}, iters={iterations:,}")


        # Make more shapes the smaller the shapes are
        #iterations = (i + 1) * 5
        for j in range(iterations):
            # calculate a random position in the image
            x = random.randint(0, cols - 1)
            y = random.randint(0, rows - 1)

            # Make a circle at (x, y) with radius radius
            # and fetch the average color in that region.
            # paint a circle with that color in the result
            # image
            mask = circle_mask(image, (x, y), radius)
            result[mask] = image[mask].mean()

    return result

def shape_params(image):
    # Unpack the shape of the array, we'll need it in the loop
    rows, cols = image.shape
    area = rows * cols

    # Start with big shapes and get progressively smaller
    radii = [256, 128, 64, 32, 16, 8]
    for i, radius in enumerate(radii):
        circle_area = math.pi * radius * radius
        iterations = int(area // circle_area)
        #print(f"i={i}, r={radius}, iters={iterations:,}")

        # Make more shapes the smaller the shapes are
        #iterations = (i + 1) * 5
        for j in range(iterations):
            # calculate a random position in the image
            x = random.randint(0, cols - 1)
            y = random.randint(0, rows - 1)

            # Make a circle at (x, y) with radius radius
            # and fetch the average color in that region.
            # paint a circle with that color in the result
            # image
            mask = circle_mask(image, (x, y), radius)
            avg_color = image[mask].mean()
            yield ('circle', x, y, radius, avg_color)

def scaling_factor(img):
    """
    calculate a scaling factor in points/pixel

    This assumes the image is in landscape orientation and will
    be mapped to a letter page (portrait) with 1-inch margins.
    """
    _, width_pixels = img.shape
    width_inches = 6.5
    points_per_inch = 72.0
    width_points = width_inches * points_per_inch
    return width_points / width_pixels

def process_shapes(params, img):
    points_per_pixel = scaling_factor(img)
    print(points_per_pixel)
    for shape, x, y, r, avg_color in params:
        x_points = x * points_per_pixel
        y_points = y * points_per_pixel
        r_points = r * points_per_pixel
        print(f'{x_points:.2f} {y_points:.2f} {r_points:.2f} circle')


def main():
    img = cv2.imread('images/gears.jpg')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Use a circle mask to select a portion of the image
    #result = paint_shapes(gray)
    #cv2.imwrite('output/circle_gears.png', result)

    process_shapes(shape_params(gray), gray)

if __name__ == '__main__':
    main()
