#!/usr/bin/env python3

'''
This script creates a dataset (table, saved as csv) of features.
The input of the script is the *output of floss on malware and benign files*.
The dataset is used to train a Logistic Regression model to classify malware and benign files.
The structure of the dataset is:
*strings_features (list of 0/1), *type_of_extraction_features (list of 0/1), is_malware (bool)
'''

from argparse import ArgumentParser
import os
import sklearn
import csv
import pandas as pd
from feature_extractor import extract_features_from_output, get_num_of_features
from tqdm import tqdm


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-m', '--malware-dir', dest='malware_dir',
                        required=True, help='the directory of the malware floss output files')
    parser.add_argument('-b', '--benign-dir', dest='benign_dir',
                        required=True, help='the directory of the benign floss output files')
    parser.add_argument('-o', '--output', dest='output_path',
                        required=True, help='the output file path')
    parser.add_argument('-sd', '--strings-dataset', dest='strings_dataset_path',
                        required=True, help='the strings dataset json file path')
    args = parser.parse_args()
    return args


def add_dir_to_dataset(dir_path, dataset, strings_dataset_path, is_malware):
    for file_name in tqdm(os.listdir(dir_path)):
        file_path = os.path.join(dir_path, file_name)
        features = extract_features_from_output(
            file_path, strings_dataset_path)
        features.append(is_malware)
        dataset.loc[len(dataset)] = features


def main():
    args = parse_args()

    num_of_features = get_num_of_features(args.strings_dataset_path)
    dataset = pd.DataFrame(columns=list(
        range(num_of_features)) + ['is_malware'])

    add_dir_to_dataset(args.malware_dir, dataset,
                       args.strings_dataset_path, True)
    add_dir_to_dataset(args.benign_dir, dataset,
                       args.strings_dataset_path, False)

    dataset.to_csv(args.output_path, encoding='utf-8', index=False)


if __name__ == '__main__':
    main()
