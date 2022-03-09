import argparse
from pathlib import Path
from typing import Iterable

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib import rcParams
from plot_likert import plot_likert

from constants import (COLUMNS, COLUMNS_ACT, COLUMNS_STREAM, LABELS_ACT, LABELS_STREAM, OPTIONS_ACT, OPTIONS_FREQUENCY,
                       OPTIONS_STREAM)

FLOAT_FORMAT = '{:0.2f}'.format


def mean_and_std(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    return pd.DataFrame({
        'mean': df[columns].mean(),
        'std': df[columns].std()
    })


def likert(df: pd.DataFrame, values: Iterable[str], labels: list[str], output_file: Path) -> None:
    df.columns = labels
    ax = plot_likert(df, list(values), label_max_width=50)
    ax.tick_params(left=False, bottom=False)
    sns.despine(ax=ax, left=True, bottom=True)
    plt.savefig(output_file, bbox_inches='tight')


def histogram(df: pd.DataFrame, columns: list[str], column_labels: list[str], values: list[str],
              output_file: Path) -> None:
    df_melted = df[columns].melt(value_vars=columns)
    g = sns.catplot(kind='count', data=df_melted, x='value', col='variable', order=values, height=3)
    g.despine(left=True, bottom=True)
    g.set_xticklabels(rotation=90)
    g.set(xlabel=None, ylabel=None)

    for ax, column_label in zip(g.axes.flat, column_labels):
        ax.set_title(column_label)
        ax.tick_params(left=False, bottom=False)

    plt.savefig(output_file, bbox_inches='tight')


def analyze(csv_file: Path, output_dir: Path, ext: str) -> None:
    rcParams['font.family'] = 'serif'
    rcParams['font.serif'] = 'Times New Roman'

    df = pd.read_csv(csv_file, header=0, names=COLUMNS)
    print(df.describe())

    output_dir.mkdir(exist_ok=True, parents=True)

    # likert
    likert(df[COLUMNS_ACT], OPTIONS_ACT.keys(), LABELS_ACT, output_dir / f'act.{ext}')
    likert(df[COLUMNS_STREAM], OPTIONS_STREAM.keys(), LABELS_STREAM, output_dir / f'stream.{ext}')

    # re- and discovery
    histogram(df,
              ['discover_new', 'discover_re_desire', 'discover_re_actual'],
              ['Dicovery of new music', 'Rediscovery (desire)', 'Rediscovery (actual)'],
              OPTIONS_FREQUENCY,
              output_dir / f'freqs.{ext}')

    df.replace(OPTIONS_ACT, inplace=True)
    df.replace(OPTIONS_STREAM, inplace=True)

    print(mean_and_std(df, COLUMNS_ACT).to_latex(float_format=FLOAT_FORMAT))
    print(mean_and_std(df, COLUMNS_STREAM).to_latex(float_format=FLOAT_FORMAT))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('csv_file', type=Path, help='CSV file downloaded from google forms')
    parser.add_argument('output_dir', type=Path, help='output directory for figures')
    parser.add_argument('--extension', type=str, default='png',
                        help='file type of generated figures, change it to pdf for vector')
    args = parser.parse_args()

    analyze(args.csv_file, args.output_dir, args.extension)
