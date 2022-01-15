import pickle
from argparse import ArgumentParser

import numpy as np
from matplotlib import pyplot as plt
from sklearn.metrics import accuracy_score

from project_name.data.load_dataset import load_dataset
from project_name.models.predict_model import predict


def load_model(model_path):
    with open(model_path, 'rb') as file:
        model = pickle.load(file)

    return model


def accuracy_plot(X_train, y_train, X_test, y_test, bayes, forest, forest_optimized):

    labels = ['bayes', 'forest', 'forest_optimized']
    x = np.arange(len(labels))
    width = 0.4

    accuracy_bayes_train = accuracy_score(y_train, predict(bayes, X_train)[1])
    accuracy_forest_train = accuracy_score(y_train, predict(forest, X_train)[1])
    accuracy_forest_optimized_train = accuracy_score(y_train, predict(forest_optimized, X_train)[1])

    accuracy_bayes_test = accuracy_score(y_test, predict(bayes, X_test)[1])
    accuracy_forest_test = accuracy_score(y_test, predict(forest, X_test)[1])
    accuracy_forest_optimized_test = accuracy_score(y_test, predict(forest_optimized, X_test)[1])

    plt.bar(x - width/2, [accuracy_bayes_train, accuracy_forest_train, accuracy_forest_optimized_train], width, label='train')
    plt.bar(x + width/2, [accuracy_bayes_test, accuracy_forest_test, accuracy_forest_optimized_test], width, label='test')

    plt.title('Model accuracy')
    plt.xticks(x, labels)
    plt.legend()

    plt.show()


def main(args):

    X_train, y_train = load_dataset(args.train_dataset)
    X_test, y_test = load_dataset(args.test_dataset)

    bayes = load_model(args.bayes)
    forest = load_model(args.forest)
    forest_optimized = load_model(args.forest_optimized)

    accuracy_plot(X_train, y_train, X_test, y_test, bayes, forest, forest_optimized)


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('--train-dataset', help='path to train dataset', default='data/processed/train.csv')
    parser.add_argument('--test-dataset', help='path to test dataset', default='data/processed/test.csv')
    parser.add_argument('--bayes', help='path to bayes model', default='models/bayes.pkl')
    parser.add_argument('--forest', help='path to random forest model', default='models/forest.pkl')
    parser.add_argument('--forest-optimized', help='path to optimized forest model', default='models/forest-optimized.pkl')

    args = parser.parse_args()
    main(args)
