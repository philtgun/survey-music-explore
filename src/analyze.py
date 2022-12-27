import argparse
from pathlib import Path
from typing import Iterable

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib import rcParams
from plot_likert import plot_likert

from constants import (COLUMNS, COLUMNS_ACT, COLUMNS_STREAM, LABELS_ACT, LABELS_STREAM, OPTIONS_ACT, OPTIONS_FREQUENCY,
                       OPTIONS_STREAM, OPTIONS_TAGS_EXPLORE, OPTIONS_TAGS_PLAYLISTS)

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


def _reverse(_dict: dict) -> dict:
    return {v: k for k, v in _dict.items()}


def count_mapped_values(df: pd.Series, values_dict: dict[str, str]) -> pd.Series:
    counts = []
    for value in values_dict.values():
        counts.append(len(df[df.str.contains(value, regex=False)]))

    return pd.Series(data=counts, index=values_dict.keys())


def analyze(tsv_file: Path, output_dir: Path, ext: str) -> None:
    # formatting
    rcParams['font.family'] = 'serif'
    rcParams['font.serif'] = 'Times New Roman'

    df = pd.read_csv(tsv_file, header=0, names=COLUMNS, delimiter='\t')

    # output dir
    output_dir.mkdir(exist_ok=True, parents=True)

    # likert
    likert(df[COLUMNS_ACT], OPTIONS_ACT.keys(), LABELS_ACT, output_dir / f'act.{ext}')
    likert(df[COLUMNS_STREAM], OPTIONS_STREAM.keys(), LABELS_STREAM, output_dir / f'stream.{ext}')

    # re- and discovery
    histogram(df,
              ['discover_new', 'discover_re_desire', 'discover_re_actual'],
              ['Discovery of new music', 'Rediscovery (desire)', 'Rediscovery (actual)'],
              OPTIONS_FREQUENCY,
              output_dir / f'freqs.{ext}')

    df.replace(OPTIONS_ACT, inplace=True)
    df.replace(OPTIONS_STREAM, inplace=True)

    # table for latex
    print(mean_and_std(df, COLUMNS_STREAM).to_latex(float_format=FLOAT_FORMAT))

    # correlations between Likert questions
    corr = df[COLUMNS_ACT + COLUMNS_STREAM].corr()
    corr.to_csv(output_dir / 'corr.csv', float_format=FLOAT_FORMAT)
    plt.figure()
    sns.heatmap(corr)
    plt.savefig(output_dir / f'corr.{ext}', bbox_inches='tight')

    # number of people that provided different values for desire and actual rediscovery
    print('Rediscovery mismatch: ', pd.value_counts(df['discover_re_desire'] != df['discover_re_actual']))

    # countries
    unique_countries = df['country'].unique()
    print(f'Unique countries {len(unique_countries)}: {unique_countries}')

    # categories that are mentioned for playlist search and discovery
    playlist_counts = count_mapped_values(df['playlist_terms'], OPTIONS_TAGS_PLAYLISTS)
    explore_counts = df['explore_terms'].value_counts().to_frame()
    explore_counts.rename(index=_reverse(OPTIONS_TAGS_EXPLORE), inplace=True)
    explore_counts = explore_counts[explore_counts.index.isin(OPTIONS_TAGS_EXPLORE.keys())]
    counts_df = pd.concat([playlist_counts, explore_counts], axis=1)
    counts_df.reset_index(inplace=True)
    counts_df.columns = ['Terms', 'Playlist searching', 'Discovery/Exploration']
    counts_df = counts_df.melt(id_vars='Terms')
    plt.figure(figsize=[4, 3])
    ax = sns.barplot(data=counts_df, x='Terms', y='value', hue='variable')
    sns.despine(bottom=True, left=True)
    ax.set(xlabel=None, ylabel=None)
    ax.tick_params(left=False, bottom=False)
    ax.get_legend().set_title(None)
    plt.xticks(rotation=90)
    plt.savefig(output_dir / f'terms.{ext}', bbox_inches='tight')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('tsv_file', type=Path, help='TSV file downloaded from google forms')
    parser.add_argument('output_dir', type=Path, help='output directory for figures')
    parser.add_argument('--extension', type=str, default='png',
                        help='file type of generated figures, change it to pdf for vector')
    args = parser.parse_args()

    analyze(args.tsv_file, args.output_dir, args.extension)
