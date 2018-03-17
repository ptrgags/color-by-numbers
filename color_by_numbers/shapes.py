"""
Shapes takes an image and generates a pattern of overlapping
"""
def configure_parser(subparsers, common):
    """
    Configure parser for the downscale subcommand
    """
    # Downscale arguments
    parser_shapes = subparsers.add_parser('shapes', parents=[common])
    parser_shapes.set_defaults(func=main)

def main(args):
    """
    Entry point for the shapes method
    """
    print("Shapes called with", args)
