import pandas as pd


def load_dataset(path: str, target_column: str = 'returned', upsample: bool = False):

    df = pd.read_csv(path)
    df = df.sample(frac=1.0)

    if upsample:
        positive = df[df[target_column] == True]
        negative = df[df[target_column] == False]

        df = pd.concat([negative, positive.sample(2 * len(positive), replace=True)], ignore_index=True)

    try:
        y = df.pop(target_column)
    except KeyError:
        y = None

    return df, y
