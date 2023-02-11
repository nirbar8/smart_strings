#!/usr/bin/env python3
'''
This script is used to print all the strings in given binary file.
- The strings are extracted using floss.
- Each string get score according to staticly analysis.
- The strings are sorted by their score.
'''

from argparse import ArgumentParser
from strings_extractor import get_strings_from_binary, get_strings_from_output
from feature_extractor import exctract_features_from_binary, extract_features_from_output

from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)


def parse_args():
    parser = ArgumentParser()

    # one of the following is required
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('-ib', '--input-binary',
                             dest='binary_file', help='the binary file to analyze')
    input_group.add_argument('-if', '--input-floss-output',
                             dest='floss_output', help='the floss output file to analyze')

    parser.add_argument('-v', '--verbose', help='print verbose output',
                        default=False, action='store_true')
    parser.add_argument('--no-color', help='print non-colored output',
                        default=False, action='store_true')
    parser.add_argument('--show-scores', help='print scores for each string',
                        default=False, action='store_true')
    args = parser.parse_args()

    return args


def main():
    args = parse_args()

    if args.binary_file:
        strings = get_strings_from_binary(args.binary_file)
    else:
        strings = get_strings_from_output(args.floss_output)

    for string in strings:
        print_string(string, args.verbose, args.no_color, args.show_scores)


def print_string(string, verbose, no_color, show_scores):
    '''
    This function prints the given string.

    Args:
        string (DataString): The string to print.
        verbose (bool): If True, print verbose output.
        no_color (bool): If True, print non-colored output.
        show_scores (bool): If True, print scores for each string.
    '''

    print(string.format_string(verbose, no_color, show_scores))


if __name__ == '__main__':
    main()
