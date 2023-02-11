import json
import os
import sklearn
import numpy as np
from sklearn.linear_model import LogisticRegression
from argparse import ArgumentParser
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import pickle

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--train-ds', dest='train_dataset_path',
                        required=True, help='the path to the train dataset (csv format)')
    parser.add_argument('--test-ds', dest='test_dataset_path', 
                        help='the path to the test dataset, if you want to evaluate the models performance (csv format)')
    parser.add_argument('-o', '--output', dest='output_path', required=True,
                        help='the path to the output file of the trained model (pickle format)')
    args = parser.parse_args()
    return args


def eval_model(model, x_test, y_test):
    y_pred = model.predict(x_test)
    y_pred_prob = model.predict_proba(x_test)[:, 1]

    print('The average score for the malicous test set is:',
          np.mean(y_pred_prob[y_test == 1]) * 100)
    print('The average score for the benign test set is:',
          np.mean(y_pred_prob[y_test == 0]) * 100)

    print()
    print(f'Accuracy: {accuracy_score(y_test, y_pred) * 100:.1f}%')
    print(f'Precision: {precision_score(y_test, y_pred) * 100:.1f}%')
    print(f'Recall: {recall_score(y_test, y_pred) * 100:.1f}%')
    print(f'F1: {f1_score(y_test, y_pred) * 100:.1f}%')


def main():
    args = parse_args()

    train_dataset = pd.read_csv(args.train_dataset_path)
    
    x_train = train_dataset.iloc[:, :-1]
    y_train = train_dataset.iloc[:, -1]

    model = LogisticRegression()
    model.fit(x_train.values, y_train.values)

    with open(args.output_path, 'wb') as f:
        pickle.dump(model, f)

    print('The trained model was saved to', args.output_path)

    if args.test_dataset_path is None:
        return

    print()
    print('Evaluating the model performance on the test set...')
    print('---------------------------------------------------')

    test_dataset = pd.read_csv(args.test_dataset_path)
    x_test = test_dataset.iloc[:, :-1].values
    y_test = test_dataset.iloc[:, -1].values
    
    eval_model(model, x_test, y_test)



if __name__ == '__main__':
    main()
