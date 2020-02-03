import numpy as np
import os
import pandas as pd
from dataworks.df_utils import inspect_df, summarize_df


def read_testdata_to_dataframe():
    cwd = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_csv(cwd + "/testdata/testdata.csv", parse_dates=["date"])

    return df


def test_inspect_df_assert_index_is_sorted():
    df = inspect_df(read_testdata_to_dataframe())
    v = df.index.values

    assert np.all(v[1:] - v[:-1] == 1)


def test_inspect_df_check_sum_of_nulls():
    df_org = read_testdata_to_dataframe()
    df_inspect = inspect_df(df_org)

    assert df_inspect["nulls"].sum() == df_org.isnull().sum().sum()


def test_summarize_df_check_sum_of_nulls():
    df_org = read_testdata_to_dataframe()
    df_summary = summarize_df(df_org)

    assert df_summary["n_nans"].sum() == df_org.isnull().sum().sum()


def test_summarize_df_check_original_column_types():
    df_org = read_testdata_to_dataframe()
    df_summary = summarize_df(df_org)

    # Types of columns in the original DataFrame
    org_col_type_names = [t.name for t in df_org.dtypes.values]

    # Count how many times each field in the "type" column in df_summary
    # occurs in the list of column types of df_org
    colcount = np.zeros(len(df_summary)).astype(np.int64)
    for idx, coltype in enumerate(df_summary["type"].values):
        colcount[idx] = org_col_type_names.count(coltype)

    # The count should match these fields in df_summary
    assert np.all(colcount == df_summary["ncols"].values)
