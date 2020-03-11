import numpy as np
import os
import pandas as pd
from pandas.api.types import is_datetime64_any_dtype, is_numeric_dtype, is_object_dtype
from sklearn.ensemble import RandomForestRegressor
import pytest

from dataworks.df_utils import (
    add_datefields,
    add_nan_columns,
    categorize_df,
    inspect_df,
    numeric_nans,
    summarize_df,
    replace_numeric_nulls,
    object_nan_to_empty,
    categorical_columns,
    apply_categories,
    split_dataset,
)

# Name of column in *.csv file to be parsed as dates
DATE_COLUMN = "date"
# Suffix appended to columns with null values
NULL_SUFFIX = "isnull"
# Suffix appended to categorized columns
CATEGORY_SUFFIX = "cat"


def read_testdata_to_dataframe():
    cwd = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_csv(
        cwd + "/testdata/testdata.csv", parse_dates=[DATE_COLUMN], index_col=0
    )

    return df


def test_provided_testdata_OK():
    """ In order for unit tests to make sense, there should be at least:
            - one date column
            - one numeric column
            - one object column
    """
    df_org = read_testdata_to_dataframe()

    is_datetime = []
    is_numeric = []
    is_object = []

    for col in df_org.columns:
        is_datetime.append(is_datetime64_any_dtype(df_org[col]))
        is_numeric.append(is_numeric_dtype(df_org[col]))
        is_object.append(is_object_dtype(df_org[col]))

    assert True in is_datetime
    assert True in is_numeric
    assert True in is_object


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


def test_add_datefields_default_behavior():
    df_org = read_testdata_to_dataframe()
    df_date = add_datefields(df_org, DATE_COLUMN)

    datefields = [
        "dayofweek",
        "dayofyear",
        "is_month_end",
        "is_month_start",
        "is_quarter_end",
        "is_quarter_start",
        "quarter",
        "week",
    ]

    for field in datefields:
        assert f"{DATE_COLUMN}_{field}" in df_date.columns.values


def test_add_datefields_drop_original():
    df_org = read_testdata_to_dataframe()
    df_date = add_datefields(df_org, DATE_COLUMN, drop_original=True)

    assert DATE_COLUMN not in df_date.columns.values


def test_add_datefields_custom_field_selection():
    CUSTOM_CHOICE = "dayofweek"

    df_org = read_testdata_to_dataframe()
    df_date = add_datefields(df_org, DATE_COLUMN, attrs=[CUSTOM_CHOICE])

    assert f"{DATE_COLUMN}_{CUSTOM_CHOICE}" in df_date.columns.values
    assert len(df_date.columns) == (len(df_org.columns) + 1)


def test_add_datefields_inplace():
    CUSTOM_CHOICE = "dayofyear"

    df_org = read_testdata_to_dataframe()
    _ = add_datefields(df_org, DATE_COLUMN, inplace=True)

    assert f"{DATE_COLUMN}_{CUSTOM_CHOICE}" in df_org.columns.values


def test_add_nan_columns_default_behavior():
    df_org = read_testdata_to_dataframe()
    df_null = add_nan_columns(df_org)

    # Returns pandas series with column name as index, boolean as values
    null_bool = df_org.isnull().sum() != 0
    null_cols = null_bool.index[null_bool.values]

    for colname in null_cols:
        assert f"{colname}_{NULL_SUFFIX}" in df_null.columns.values


def test_add_nan_columns_custom_field_selection():
    CUSTOM_CHOICE = "setting"

    df_org = read_testdata_to_dataframe()
    df_null = add_nan_columns(df_org, column_list=[CUSTOM_CHOICE])

    assert f"{CUSTOM_CHOICE}_{NULL_SUFFIX}" in df_null.columns.values
    assert len(df_null.columns) == (len(df_org.columns) + 1)


def test_add_nan_columns_inplace():
    CUSTOM_CHOICE = "setting"

    df_org = read_testdata_to_dataframe()
    _ = add_nan_columns(df_org, column_list=[CUSTOM_CHOICE], inplace=True)

    assert f"{CUSTOM_CHOICE}_{NULL_SUFFIX}" in df_org.columns.values


def test_numeric_nans_default_behavior():
    df_org = read_testdata_to_dataframe()
    df_inspect = inspect_df(df_org)
    df_numeric = numeric_nans(df_org)

    numeric_cols = df_inspect[df_inspect["is_numeric"]]["column"].values

    for col in numeric_cols:
        df_inspect_nulls = df_inspect[df_inspect["column"] == col]["nulls"].values[0]
        # These could contain zero nulls, depending on the test data
        if df_inspect_nulls > 0:
            df_numeric_nulls = df_numeric[df_numeric["column"] == col]["nulls"].values[
                0
            ]
            assert col in df_numeric["column"].values
            assert df_numeric_nulls == df_inspect_nulls
        else:
            assert col not in df_numeric["column"].values


def test_categorize_df_object_columns_categorized():
    df_org = read_testdata_to_dataframe()
    (df_cat, _) = categorize_df(df_org)

    org_cols = df_org.columns.values
    is_object = []

    for col in org_cols:
        is_object.append(is_object_dtype(df_org[col]))

    object_cols = org_cols[is_object]

    for col in object_cols:
        assert f"{col}_{CATEGORY_SUFFIX}" in df_cat.columns.values


def test_pipeline_integration_with_scikit_learn():
    DATA_COLUMN = "y_data"

    df_org = read_testdata_to_dataframe()
    df_test = replace_numeric_nulls(df_org)
    df_test = object_nan_to_empty(df_test)
    df_test = categorical_columns(df_test)
    df_test = apply_categories(df_test, drop=True)
    df_test = add_datefields(df_test, "date", drop_original=True)

    # Add column with 'dependent variable'
    df_test[DATA_COLUMN] = np.arange(len(df_test))
    # Split variable out again
    X_data, y_data = split_dataset(df_test, DATA_COLUMN)

    model = RandomForestRegressor(n_estimators=2, n_jobs=1, max_depth=3)
    model.fit(X_data, y_data)


def test_pipeline_integration_with_scikit_learn_missing_step_should_fail():
    """ The purpose of this test is to make sure that
        test_pipeline_integration_with_scikit_learn() will fail if the data is
        not processed correctly
    """
    DATA_COLUMN = "y_data"

    df_org = read_testdata_to_dataframe()
    df_test = replace_numeric_nulls(df_org)
    df_test = object_nan_to_empty(df_test)
    df_test = categorical_columns(df_test)
    # df_test = apply_categories(df_test, drop=True)
    df_test = add_datefields(df_test, "date", drop_original=True)

    # Add column with 'dependent variable'
    df_test[DATA_COLUMN] = np.arange(len(df_test))
    # Split variable out again
    X_data, y_data = split_dataset(df_test, DATA_COLUMN)

    model = RandomForestRegressor(n_estimators=2, n_jobs=1, max_depth=3)
    with pytest.raises(Exception):
        model.fit(X_data, y_data)
