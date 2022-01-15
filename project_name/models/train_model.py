import pickle
import logging
from argparse import Action
from argparse import ArgumentParser

from sklearn.naive_bayes import ComplementNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import balanced_accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score

from project_name.data.load_dataset import load_dataset
from project_name.models.predict_model import predict

logger = logging.getLogger(__name__)


class ParamDict(Action):
    def __call__(self, parser, namespace,
                 values, option_string=None):
        setattr(namespace, self.dest, dict())

        for value in values:
            param, param_values = value.split('=')

            if param_values.startswith('['):
                param_values = list(map(int, param_values[1:-1].split(',')))
            else:
                param_values = param_values[1:-1].split(',')

            getattr(namespace, self.dest)[param] = param_values


def model_performance(model, X, y, dataset_name: str):

    X, predictions = predict(model, X)

    logger.info('Performance on {} dataset: balanced_accuracy - {:.3f}, precision - {:.3f}, recall - {:.3f}'.format(
        dataset_name,
        balanced_accuracy_score(y, predictions),
        precision_score(y, predictions),
        recall_score(y, predictions)
    ))


def main(args):

    model = ComplementNB() if args.model == 'bayes' else RandomForestClassifier(class_weight='balanced')

    logger.info('Loading dataset at path {}'.format(args.dataset_path))
    X_train, y_train = load_dataset(args.dataset_path)
    if args.test:
        X_test, y_test = load_dataset(args.test)

    logger.info('Training started...')
    if args.optimize:
        model = GridSearchCV(model, param_grid=args.params)

    model.fit(X_train, y_train)

    if args.optimize:
        logger.info('Best model parameters: {}'.format(model.best_params_))

    model_performance(model, X_train, y_train, 'train')
    if args.test:
        model_performance(model, X_test, y_test, 'test')
    logger.info('Training finished')

    logger.info('Saving model at {}'.format(args.save_path))
    with open(args.save_path, 'wb') as file:
        pickle.dump(model, file)


if __name__ == '__main__':

    log_fmt = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    parser = ArgumentParser()

    parser.add_argument('dataset_path', help='path to train csv dataset', default='data/processed/train.csv')
    parser.add_argument('--test', help='path to test csv dataset', default='data/processed/test.csv')
    parser.add_argument('--save-path', help='path to save model', default='models/model.pkl')
    parser.add_argument('--model', choices=['bayes', 'forest'], default='bayes')
    parser.add_argument('--optimize', help='Perform gird search to optimize model accuracy', action='store_true')
    parser.add_argument('--params', nargs='*', action=ParamDict)

    args = parser.parse_args()
    main(args)
