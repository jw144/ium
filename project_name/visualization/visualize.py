import pickle
from argparse import ArgumentParser

from matplotlib import pyplot as plt
from sklearn.metrics import accuracy_score

from project_name.data.load_dataset import load_dataset
from project_name.models.predict_model import predict


def load_model(model_path):
    with open(model_path, 'rb') as file:
        model = pickle.load(file)

    return model


def accuracy_plot(X, y, bayes, forest, forest_optimized):
    accuracy_bayes = accuracy_score(y, predict(bayes, X)[1])
    accuracy_forest = accuracy_score(y, predict(forest, X)[1])
    accuracy_forest_optimized = accuracy_score(y, predict(forest_optimized, X)[1])

    plt.bar(['bayes', 'forest', 'forest_optimized'], [accuracy_bayes, accuracy_forest, accuracy_forest_optimized])
    plt.show()


def main(args):

    X, y = load_dataset(args.dataset_path)

    bayes = load_model(args.bayes)
    forest = load_model(args.forest)
    forest_optimized = load_model(args.forest_optimized)

    accuracy_plot(X, y, bayes, forest, forest_optimized)


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('--dataset_path', help='path to test dataset', default='data/processed/test.csv')
    parser.add_argument('--bayes', help='path to bayes model', default='models/bayes.pkl')
    parser.add_argument('--forest', help='path to random forest model', default='models/forest.pkl')
    parser.add_argument('--forest-optimized', help='path to optimized forest model', default='models/forest-optimized.pkl')

    args = parser.parse_args()
    main(args)
