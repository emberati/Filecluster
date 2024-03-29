from argparse import ArgumentParser, Namespace
import os


def create_parser():
    """
    Creating and configuring bundled argument parser, with prefix '-'.
    It's also able to add any prefix chars, such as '/' for windows.
    """
    parser = ArgumentParser(prefix_chars='-')
    parser.add_argument(  # Adding into parser an argument, which will be expected in command line
        '-d', '--dir', required=False, default=os.getcwd()  # Getting current working directory
    )  # It's able to change <required> to True, to make almost one argument required for command (In this case dir)
    parser.add_argument('-f', '--fast', required=False, default=False)
    return parser


class Config:
    def __init__(self, args: Namespace):
        self.fast_scanning = args.fast
        self.path = args.dir


__parser__  = create_parser()
# When parser is ready, - parse command line arguments and then getting specified dir or return current
__namespace__    = __parser__.parse_args()

config = Config(__namespace__)
