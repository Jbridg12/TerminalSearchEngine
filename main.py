'''
Josh Bridges
main.py

Driver code reads arguments and creates the relevant Search Engine instance.

'''
import sys
import engine as e
import argparse as ap

# Create class to represent errors with user providede arguments
class Error(Exception):
    """Base class for exceptions in this module."""
    pass
class ArgError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


# Create argument parser with specified args for this project
parser = ap.ArgumentParser(description='Use a Search Engine')
parser.add_argument('-root', required=True)
parser.add_argument('-mode', choices=['C','I'], required=True)
parser.add_argument('-query', nargs='?', const='a', default='a')
parser.add_argument('-verbose', nargs='?', const='T', default='F', choices=['T','F'])

# Parse sys.argv
args = parser.parse_args()

# Check to make sure a query is provided in Command Line mode
if args.mode == 'C' and args.query == 'a':
    raise ArgError(' '.join(sys.argv), "Command line mode requires query argument be specified.")

root = args.root
mode = args.mode
query = args.query

# Convert verbose to the proper boolean
if args.verbose == 'T':
    verbose = True
else:
    verbose = False

# Start your engines
# Depth is the last parameter and may be changed for drastically different url amounts and runtimes
a = e.SearchEngine(mode, verbose, query, root, 1)
a.listen()