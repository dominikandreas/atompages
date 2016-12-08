import sys

def return_variables(*args):
    return dict([tuple(arg.split("=")[:2]) for arg in sys.argv if "=" in arg])
