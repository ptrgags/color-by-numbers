#!/usr/bin/env python
"""
This is a prototype of my color-by-numbers script. I still need to plan this
out more.
"""
import cv2

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

if __name__ == '__main__':
    main()
