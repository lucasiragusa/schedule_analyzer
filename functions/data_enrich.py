import pandas as pd 
from functools import lru_cache
from utils.config import HUB

def add_day_eight(df, day_column='Dep Day'):
    """
    Creates a copy of entries for day 1 and adds them as day 8 
    to catch Sunday to Monday connections.

    Parameters:
    df (pandas.DataFrame): The DataFrame to process.
    day_column (str): The name of the column representing the day.

    Returns:
    pandas.DataFrame: The DataFrame with day 8 added.
    """
    df_temp = df[df[day_column] == 1].copy()
    df_temp[day_column] = 8

    # Using pd.concat to append df_temp to df
    return pd.concat([df, df_temp], ignore_index=True)


def add_movement_flag(df, orig_column = 'Orig'):
    """
    Adds a movement flag to the DataFrame based on the origin column.
    If the origin is not equal to the global HUB, it's an arrival; otherwise, it's a departure.

    Parameters:
    df (pandas.DataFrame): The DataFrame to which the flag will be added.
    orig_column (str): The name of the column indicating the origin.

    Returns:
    pandas.DataFrame: The DataFrame with the movement flag added.
    """
    df['movement_flag'] = df.apply(lambda x: 'Arr' if x[orig_column] != HUB else 'Dep', axis=1)
    return df


