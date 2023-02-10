import os
import json
from DataString import DataString
import sys
import subprocess


def get_strings_from_binary(binary_path):
    '''
    This function returns all the strings from the given binary file.

    Args:
        binary_path (str): The path to the binary file.

    Returns:
        list: A list of DataString objects.
    '''
    # TODO: test on vm

    output_path = os.path.join(
        os.getcwd(), f'.temp_output_{os.getpid()}.json')
    floss_args = ['floss', '-j', binary_path, '-o', output_path]
    subprocess.run(floss_args, stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)
    strings = get_strings_from_output(output_path)
    os.remove(output_path)

    return strings


def get_strings_from_output(output_path):
    '''
    This function returns all the strings from the given output file.

    Args:
        output_path (str): The path to the output file.

    Returns:
        list: A list of DataString objects.
    '''

    with open(output_path, 'r') as f:
        data = json.load(f)
    return get_strings(data)


def get_strings(output_json):
    '''
    This function returns all the strings from the given output json.

    Args:
        output_json (dict): The output json.

    Returns:
        list: A list of DataString objects.
    '''

    strings = []
    for str_type, string_lst in output_json['strings'].items():
        for string_obj in string_lst:
            ds = DataString(string_obj['string'], str_type)
            strings.append(ds)

    return sorted(strings, reverse=True)
