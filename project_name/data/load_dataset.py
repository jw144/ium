import pandas as pd


def load_dataset(path: str, target_column: str = 'returned'):

    df = pd.read_csv(path)
    y = df.pop(target_column)

    return df, y
