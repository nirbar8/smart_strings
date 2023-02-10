'''
This module contains feature extractor for binary files.
It uses floss to extract the strings from the binary file and then it uses the strings dataset to create features vector.
The features are the if binary contains or not a string from the strings dataset (which created by looking at frequent strings in malwares).
'''

import json
import os
import subprocess
import sys

from strings_extractor import get_strings_from_binary, get_strings_from_output


def load_strings_dataset(strings_dataset_path):
    '''
    This function returns the dataset from the given strings_dataset file.

    Args:
        strings_dataset_path (str): The path to the strings_dataset file.

    Returns:
        dictionary: A dictionary of { string : {"suspicious_score": float, "frequency_score": float} }.
    '''

    with open(strings_dataset_path, 'r') as f:
        return json.load(f)['strings']


def exctract_features_from_binary(binary_path, strings_dataset_path):
    '''
    This function returns the features vector of the given binary file.

    Args:
        binary_path (str): The path to the binary file.
        strings_dataset_path (str): The path to the strings_dataset file.

    Returns:
        list: A list of features.
    '''

    strings = get_strings_from_binary(binary_path)
    strings_dataset = load_strings_dataset(strings_dataset_path)

    return get_features_vector(strings, strings_dataset)


def extract_features_from_output(output_path, strings_dataset_path):
    '''
    This function returns the features vector of the given output file.

    Args:
        output_path (str): The path to the output file.
        strings_dataset_path (str): The path to the strings_dataset file.

    Returns:
        list: A list of features.
    '''

    strings = get_strings_from_output(output_path)
    strings_dataset = load_strings_dataset(strings_dataset_path)

    return get_features_vector(strings, strings_dataset)


def get_features_vector(strings, strings_dataset):
    '''
    This function returns the features vector of the given strings and strings_dataset.

    Args:
        strings (list): A list of DataString objects.
        strings_dataset (dictionary): A dictionary of { string : {"suspicious_score": float, "frequency_score": float} }.

    Returns:
        list: A list of features.
    '''

    strings_dataset_list = list(strings_dataset.keys())
    strings_features = [0] * len(strings_dataset_list)

    # strings features - for each string in input file, check if it is in the dataset (so it suspicious)
    for string in strings:
        if string.string in strings_dataset_list:
            strings_features[strings_dataset_list.index(string.string)] = 1

    # type features - if the file contains decoded string, stack string or tight string
    type_features = [0] * 3
    for string in strings:
        if string.type_of_extraction == 'decoded_string':
            type_features[0] = 1
        elif string.type_of_extraction == 'stack_string':
            type_features[1] = 1
        elif string.type_of_extraction == 'tight_string':
            type_features[2] = 1

    return strings_features + type_features


def get_num_of_features(strings_dataset_path):
    '''
    This function returns the number of features for each input file.

    Args:
        strings_dataset_path (str): The path to the strings_dataset file.

    Returns:
        int: The number of features.
    '''

    strings_dataset = load_strings_dataset(strings_dataset_path)
    return len(strings_dataset) + 3
