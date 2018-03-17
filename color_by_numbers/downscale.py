"""
Downscale is the simplest form of turning an image into a color-by-numbers page.
It downsamples the image and computes the average color in each block.
"""

def configure_parser(subparsers, common):
    """
    Configure parser for the downscale subcommand
    """
    parser_ds = subparsers.add_parser('downscale', parents=[common])
    parser_ds.set_defaults(func=main)

def main(args):
    """
    Entry point for the downscal
    """
    print("Downscale called with", args)
