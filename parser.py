# TODO: check doc
# This module is responsible for parsing the output files from floss and creating
# representation of the dataset that can be used for training and testing.

import os
import json
from DataString import DataString

from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)


def print_strings(output_path):
    '''
    This function prints all the strings in the output file.

    Args:
        output_path (str): The path to the output file.
    '''

    with open(output_path, 'r') as f:
        data = json.load(f)

    strings = []
    for str_type, string_lst in data['strings'].items():
        for string_obj in string_lst:
            ds = DataString(string_obj['string'], str_type)
            strings.append(ds)

    for ds in sorted(strings, reverse=True):
        print(ds)


# TODO: add argparse and main
if __name__ == '__main__':
    parser = print_strings(
        'floss_output/malwares_lab-1-samples_Lab01-02.exe.json')
