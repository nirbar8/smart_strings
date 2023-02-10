'''
This script creates a dataset (dictionary, saved as json) of strings.
The input of the script is the *output of floss on malware and benign files*.
The dataset is used to analyze new strings and determine if they are related to already seen malwares.
The structure of the dataset is:
    {
        'string': {
            suspicious_score: float,
            malwares_files: List[str],
            benign_files: List[str]
        }
    }
'''

from tqdm import tqdm
import json
from argparse import ArgumentParser
import sys
from DataString import DataString
import os


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-m', '--malware-dir', dest='malware_dir',
                        required=True, help='the directory of the malware floss output files')
    parser.add_argument('-b', '--benign-dir', dest='benign_dir',
                        required=True, help='the directory of the benign floss output files')
    parser.add_argument('-o', '--output', dest='output',
                        required=True, help='the output file path')
    args = parser.parse_args()
    return args


def init_string(data_string, dataset_strings):
    dataset_strings[data_string.string] = {
        'suspicious_score': data_string.scores['suspicous_text_score'],
        'malware_files': [],
        'benign_files': []
    }


def insert_string(data_string, dataset_strings, is_malware, file):
    if data_string.string not in dataset_strings:
        init_string(data_string, dataset_strings)
    if is_malware:
        dataset_strings[data_string.string]['malware_files'].append(file)
    else:
        dataset_strings[data_string.string]['benign_files'].append(file)


def scan_dir(dataset, dir_path, is_malware, dataset_output_path):
    for idx, file in enumerate(tqdm(os.listdir(dir_path))):

        if file in dataset['scanned_files']:
            print(f'skip idx={idx}', end='\r')
            continue
        dataset['scanned_files'].append(file)

        dataset_strings = dataset['strings']
        file_path = os.path.join(dir_path, file)
        with open(file_path, 'r') as f:
            output_json = json.load(f)
            for str_type, string_lst in output_json['strings'].items():
                for string_obj in string_lst:
                    data_string = DataString(string_obj['string'], str_type)
                    insert_string(data_string, dataset_strings,
                                  is_malware, file)

        if idx % 10 == 0:
            dump_dataset(dataset, dataset_output_path)

    dump_dataset(dataset, dataset_output_path)


def dump_dataset(dataset, output_path):
    with open(output_path, 'w') as f:
        json.dump(dataset, f, indent=4)


def main():
    args = parse_args()

    # checkpoint restore
    if os.path.exists(args.output):
        with open(args.output, 'r') as f:
            dataset = json.load(f)
    else:
        dataset = {'scanned_files': [], 'strings': {}}

    scan_dir(dataset, args.malware_dir, True, args.output)
    scan_dir(dataset, args.benign_dir, False, args.output)


if __name__ == '__main__':
    main()
