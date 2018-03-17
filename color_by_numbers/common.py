import cv2

def debug_save(fname, image, args):
    """
    if --debug is specified, save an extra image in output/debug
    """
    if args.debug:
        full_fname = 'output/debug/{}'.format(fname)
        cv2.imwrite(full_fname, image)
