import numpy as np
import os
import pandas as pd
from dataworks.df_utils import inspect_df


def read_and_inspect():
    cwd = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_csv(cwd + "/testdata/testdata.csv", parse_dates=["date"])

    return inspect_df(df)


def test_inspect_df_index_sorted():
    df = read_and_inspect()
    v = df.index.values

    assert np.all(v[1:] - v[:-1] == 1)
