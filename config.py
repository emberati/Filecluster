import argparse as ap
import os


def get_path():
    path = os.getcwd()  # Getting current working directory

    '''
    Creating bundled argument parser, with prefix '-'.
    It's also able to add any prefix chars, such as '/' for windows.
    '''
    parser = ap.ArgumentParser(prefix_chars='-')
    parser.add_argument(  # Adding into parser an argument, which will be expected in command line
        '-d', '--dir', required=False, default=path
    )  # It's able to change <required> to True, to make almost one argument required for command (In this case dir)

    # When parser ready, - parse command line arguments and then getting specified dir (if specified) or return current
    args = parser.parse_args()
    if args.dir: path = args.dir

    return path
