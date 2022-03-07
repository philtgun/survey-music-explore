import argparse
from pathlib import Path

import pandas as pd

from constants import COLUMNS, COLUMNS_ACT, COLUMNS_STREAM, OPTIONS_ACT, OPTIONS_STREAM

FLOAT_FORMAT = '{:0.2f}'.format


def mean_and_std(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    return pd.DataFrame({
        'mean': df[columns].mean(),
        'std': df[columns].std()
    })


def analyze(csv_file: Path) -> None:
    df = pd.read_csv(csv_file, header=0, names=COLUMNS)

    df.replace(OPTIONS_ACT, inplace=True)
    df.replace(OPTIONS_STREAM, inplace=True)

    print(mean_and_std(df, COLUMNS_ACT).to_latex(float_format=FLOAT_FORMAT))
    print(mean_and_std(df, COLUMNS_STREAM).to_latex(float_format=FLOAT_FORMAT))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('csv_file', help='CSV file downloaded from google forms')
    args = parser.parse_args()

    analyze(args.csv_file)
