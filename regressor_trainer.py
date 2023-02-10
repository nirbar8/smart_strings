import json
import os
import sklearn
import numpy as np
from sklearn.linear_model import LogisticRegression
from argparse import ArgumentParser
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-d', '--dataset', dest='dataset_path',
                        required=True, help='the dataset csv file path')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    dataset = pd.read_csv(args.dataset_path)
    x = dataset.iloc[:, :-1]
    y = dataset.iloc[:, -1]

    # x_train, x_test, y_train, y_test = train_test_split(
    #     x, y, test_size=0.2, random_state=42, stratify=y)

    model = LogisticRegression()
    model.fit(x, y)

    y_pred = model.predict(x)
    y_pred_prob = model.predict_proba(x)[:, 1]

    print('The average score for the malicous test set is:',
          np.mean(y_pred_prob[y == 1]))
    print('The average score for the benign test set is:',
          np.mean(y_pred_prob[y == 0]))

    print('Accuracy:', accuracy_score(y, y_pred))
    print('Precision:', precision_score(y, y_pred))
    print('Recall:', recall_score(y, y_pred))
    print('F1:', f1_score(y, y_pred))


if __name__ == '__main__':
    main()
