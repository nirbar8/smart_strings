#!/usr/bin/env python3

from feature_extractor import exctract_features_from_binary, extract_features_from_output
from argparse import ArgumentParser
import pickle

def parse_args():
    parser = ArgumentParser()
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('-ib', '--input-binary', dest='input_binary_path',
                                help='the path to the input binary')
    input_group.add_argument('-if', '--input-floss-output', dest='input_floss_output_path',
                                help='the path to the floss result file (json)')
    parser.add_argument('-m', '--model', dest='model_path', default='data/model.pickle',
                        help='the path to the trained model (pickle format)')
    parser.add_argument('-sd', '--strings-dataset', dest='strings_dataset_path', default='data/strings_dataset.json',
                        help='the path to the strings dataset (json format)')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    model = load_model(args.model_path)

    if args.input_binary_path is not None:
        features = exctract_features_from_binary(args.input_binary_path, args.strings_dataset_path)
    else:
        features = extract_features_from_output(args.input_floss_output_path, args.strings_dataset_path)

    score = eval_score(model, features)
    print(f'The score for the file is {score:.1f}')


def load_model(model_path):
    with open(model_path, 'rb') as f:
        return pickle.load(f)


def eval_score(model, features):
    return model.predict_proba([features])[0, 1] * 100


if __name__ == '__main__':
    main()