import numpy as np
import pandas as pd

from collections import OrderedDict
from pandas.api.types import is_numeric_dtype
from typing import Any, Iterable


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
