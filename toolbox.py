# Library Import

import numpy as np
import pandas as pd

def add_missing_dates(data):
    """
    This function returns a new DataFrame with the missing dates.

    Parameters
    ----------
    data: DataFrame
        A DataFrame with missing dates.

    Returns
    -------
    DataFrame
        A new DataFrame with all dates.
    """

    missing_dates = set(pd.date_range(data["date"].min(), data["date"].max())) - set(data["date"])
    missing_data = pd.DataFrame({"date": list(missing_dates), "price": np.NaN})
    new_data = data.append(missing_data, ignore_index=True)
    new_data = new_data.sort_values(by="date")
    new_data = new_data.reset_index(drop=True)
    new_data = fill_missing_values(new_data)
    return new_data

def fill_missing_values(data):
    """
    This function returns a new DataFrame without missing values.

    Parameters
    ----------
    data: DataFrame
        A DataFrame with missing values.

    Returns
    -------
    DataFrame
        A new DataFrame without missing values.
    """

    data_copy = data.copy()
    for index in range(1, data_copy.shape[0]):
        current_price, previous_price = data_copy.loc[index, "price"], data_copy.loc[index - 1, "price"]
        data_copy.loc[index, "price"] = previous_price if pd.isna(current_price) else current_price
    return data_copy

def get_simple_moving_average(data, n):
    """
    This function returns the result of n days simple moving average.

    Parameters
    ----------
    data: DataFrame
        A DataFrame with prices.

    n: int
        Number of days.

    Returns
    -------
    DataFrame
        A new DataFrame with the results of simple moving average.
    """

    data_copy = data.copy()
    simple_moving_average = data_copy.rolling(n).mean()
    new_data = pd.DataFrame({"date": data_copy["date"], "price": simple_moving_average["price"]})
    new_data = new_data.dropna()
    new_data = new_data.reset_index(drop=True)
    return new_data

def append_data(data_one, data_two, data_one_label, data_two_label):
    """
    This function appends one DataFrame with another.

    Parameters
    ----------
    data_one: DataFrame
        A DataFrame.

    data_two: DataFrame
        A DataFrame.

    data_one_label: str
        DataFrame one label.

    data_two_label: str
        DataFrame two label.

    Returns
    -------
    DataFrame
        A new DataFrame that contains both DataFrames information.
    """

    data_one_copy = data_one.copy()
    data_two_copy = data_two.copy()
    new_data_one = add_column(data_one_copy, data_one_label)
    new_data_two = add_column(data_two_copy, data_two_label)
    new_data = new_data_one.append(new_data_two, ignore_index=True)
    new_data = new_data.sort_values(by="date")
    new_data = new_data.reset_index(drop=True)
    return new_data


def add_column(data, column):
    """
    This function returns a DataFrame with a new column.

    Parameters
    ----------
    data: DataFrame
        A DataFrame.
    column: str
        Column name.

    Returns
    -------
    DataFrame
        A new DataFrame with a new column.
    """
    data_copy = data.copy()
    new_data = data_copy.assign(oil_type = column)
    return new_data