import argparse as ap
import os


path = os.getcwd()


def create_parser():
    parser = ap.ArgumentParser(prefix_chars='-')    # Also it's able to add any prefix chars, such as '/' for windows
    parser.add_argument('-d', '--dir', required=False, default=path)  # It's able to change <required> to True, to prevent root directory searching
    return parser


def __init__():
    global path
    parser = create_parser()
    namespace = parser.parse_args()

    path = namespace.dir


__init__()
