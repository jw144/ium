import pandas as pd


def load_dataset(path: str, target_column: str = 'returned'):

    df = pd.read_csv(path)
    try:
        y = df.pop(target_column)
    except KeyError:
        y = None

    return df, y
