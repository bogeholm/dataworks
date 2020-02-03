import numpy as np
import pandas as pd

from collections import OrderedDict
from pandas.api.types import is_numeric_dtype
from typing import List, Optional, Tuple


def inspect_df(df: pd.DataFrame) -> pd.DataFrame:
    """ Show column types and null values in DataFrame df
    """
    if len(df) == 0:
        print("Empty DataFrame")
        return

    resdict = OrderedDict()

    # Inspect nulls
    null_series = df.isnull().sum()
    resdict["column"] = null_series.index
    resdict["null_fraction"] = np.round(null_series.values / len(df), 3)
    resdict["nulls"] = null_series.values
    # Inspect types
    types = df.dtypes.values
    type_names = [t.name for t in types]
    resdict["type"] = type_names
    # Is numeric?
    is_numeric = []
    for col in df.columns:
        is_numeric.append(is_numeric_dtype(df[col]))
    resdict["is_numeric"] = is_numeric
    # Dataframe
    resdf = pd.DataFrame(resdict)
    resdf.sort_values("null_fraction", inplace=True)
    resdf.reset_index(inplace=True, drop=True)

    return resdf


def summarize_df(df: pd.DataFrame) -> pd.DataFrame:
    """ Show stats;
        - rows:
            - column types
        - columns
            - number of columns
            - number of cols containing NaN's
    """
    # Original DataFrame
    (nrows, _) = df.shape
    # Stats of DataFrame
    stats = inspect_df(df)
    data_types = np.unique(stats["type"].values)

    resdict = OrderedDict()

    # Column: data types
    resdict["type"] = data_types

    ncols_type = []
    ncols_nan = []
    n_nans = []
    n_total = []

    for dt in data_types:
        # Column: number of columns with type
        nc = len(stats[stats["type"] == dt])
        ncols_type.append(nc)

        # Column: number of columns with NaNs
        nan_cols = stats[(stats["type"] == dt) & stats["nulls"] > 0]
        ncols_nan.append(len(nan_cols))

        # Column: number of NaNs
        n_nans.append(nan_cols["nulls"].sum())

        # Column: total number of values
        n_total.append(nc * nrows)

    # Prepare dict for the df
    resdict["ncols"] = ncols_type
    resdict["ncols_w_nans"] = ncols_nan
    resdict["n_nans"] = n_nans
    resdict["n_total"] = n_total

    # Proportions of NaNs in each column group.
    # Division by zero shouldn't occur
    nan_frac = np.array(n_nans) / np.array(n_total)
    resdict["nan_frac"] = np.round(nan_frac, 2)

    resdf = pd.DataFrame(resdict)
    resdf.sort_values("type", inplace=True)
    resdf.reset_index(inplace=True, drop=True)

    return resdf


def add_datefields(
    df: pd.DataFrame,
    column: str,
    drop_original: bool = False,
    inplace: bool = False,
    attrs: Optional[List[str]] = None,
) -> pd.DataFrame:
    """ Add attributes of the date to dataFrame df
    """
    raw_date = df[column]

    # Pandas datetime attributes
    if attrs is None:
        attributes = [
            "dayofweek",
            "dayofyear",
            "is_month_end",
            "is_month_start",
            "is_quarter_end",
            "is_quarter_start",
            "quarter",
            "week",
        ]
    else:
        attributes = attrs

    # Return new?
    if inplace:
        resdf = df
    else:
        resdf = df.copy(deep=True)

    # Could probably be optimized with pd.apply()
    for attr in attributes:
        new_column = f"{column}_{attr}"
        # https://stackoverflow.com/questions/2612610/
        new_vals = [getattr(d, attr) for d in raw_date]
        resdf[new_column] = new_vals

    if drop_original:
        resdf.drop(columns=column, inplace=True)

    return resdf


def add_nan_columns(
    df: pd.DataFrame, inplace: bool = False, column_list: Optional[List[str]] = None
) -> pd.DataFrame:
    """ For each column containing NaNs, add a boolean
        column specifying if the column is NaN. Can be used
        if the data is later imputated.
    """
    if column_list is not None:
        nan_columns = column_list
    else:
        # Get names of columns containing at least one NaN
        temp = df.isnull().sum() != 0
        nan_columns = temp.index[temp.values]

    # Return new?
    if inplace:
        resdf = df
    else:
        resdf = df.copy(deep=True)

    for column in nan_columns:
        new_column = f"{column}_isnull"
        nans = df[column].isnull()
        resdf[new_column] = nans

    return resdf


def numeric_nans(df: pd.DataFrame) -> pd.DataFrame:
    """ Inspect numerical NaN values of a DataFrame df
    """
    stats = inspect_df(df)
    nan_stats = stats.loc[stats["is_numeric"] & (stats["nulls"] > 0)].copy(deep=True)

    len_uniques = []
    uniques = []

    for row in nan_stats["column"].values:
        uniq = np.unique(df[row][df[row].notnull()].values)
        len_uniques.append(len(uniq))
        uniques.append(uniq)

    nan_stats["num_uniques"] = len_uniques
    nan_stats["uniques"] = uniques
    nan_stats.reset_index(inplace=True, drop=True)

    return nan_stats


def categorize_df(
    df: pd.DataFrame,
    columns: Optional[List[str]] = None,
    inplace: bool = False,
    drop_original: bool = True,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """ Categorize values in columns, and replace value with category.
        If no columns are given, default to all 'object' columns
    """
    if columns is not None:
        cat_cols = columns
    else:
        cat_cols = df.columns[[dt.name == "object" for dt in df.dtypes.values]]

    if inplace:
        resdf = df
    else:
        resdf = df.copy(deep=True)

    df_codes = []
    df_cats = []
    n_categories = []

    for column in cat_cols:
        new_column = f"{column}_category"
        cat_column = df[column].astype("category")
        # By default, NaN is -1. We convert to zero by incrementing all.
        col_codes = cat_column.cat.codes + 1
        resdf[new_column] = col_codes

        # DataFrame with the codes
        df_codes.append(col_codes)
        df_cats.append(cat_column.cat.categories)
        n_categories.append(len(np.unique(col_codes)))

    cat_dict = OrderedDict()
    cat_dict["column"] = cat_cols
    # MyPy picks up an error in the next line. Bug is where?
    cat_dict["n_categories"] = n_categories  # type: ignore[assignment]
    cat_dict["categories"] = df_cats
    cat_dict["codes"] = df_codes
    cat_df = pd.DataFrame(cat_dict)

    if drop_original:
        resdf.drop(columns=cat_cols, inplace=True)

    return (resdf, cat_df)
