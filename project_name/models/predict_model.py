import pickle
import logging
import pandas as pd
from argparse import ArgumentParser

from project_name.data.load_dataset import load_dataset


def predict(model, data):

    if isinstance(data, str):
        X, _ = load_dataset(data)
    else:
        X = data

    return X, model.predict(X)


def main(args):

    logger = logging.getLogger(__name__)

    logger.info('Loading model from {}'.format(args.model_path))
    with open(args.model_path, 'rb') as file:
        model = pickle.load(file)

    logger.info('Predicting on data from {}'.format(args.dataset_path))
    X, predictions = predict(model, args.dataset_path)

    X[args.save] = pd.Series(predictions, index=X.index)
    X.to_csv(args.dataset_path, index=False)

    if args.print:
        print(X.head(len(X)))


if __name__ == '__main__':

    log_fmt = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    parser = ArgumentParser()

    parser.add_argument('model_path', help='path to pickled model used during prediction', default='models/model.pkl')
    parser.add_argument('dataset_path', help='path to evaluation csv dataset', default='data/processed/test.csv')
    parser.add_argument('--save', help='add column in dataset and save results in that column', default='returned')
    parser.add_argument('--print', help='print result in console', action='store_true')

    args = parser.parse_args()
    main(args)
