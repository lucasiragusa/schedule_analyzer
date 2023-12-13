from functools import lru_cache

@lru_cache(maxsize=None)  # Infinite cache size. Adjust as needed.
def convert_decimal_to_time(decimal_time):
    sign = "-" if decimal_time < 0 else ""
    total_minutes = round(abs(decimal_time) * 24 * 60)
    # Rounding to the nearest 5 minutes
    total_minutes = round(total_minutes / 5) * 5
    hours, minutes = divmod(total_minutes, 60)
    # Modulo 24 in case the decimal_time was > 1
    hours = hours % 24
    return f"{sign}{int(hours):02d}:{int(minutes):02d}"

def datetime_to_day_fraction(dt):
    total_seconds = dt.hour * 3600 + dt.minute * 60 + dt.second
    total_seconds_in_day = 24 * 60 * 60
    return total_seconds / total_seconds_in_day

def convert_time_columns_to_fraction(df, columns):
    """
    Converts specified time columns of a DataFrame from datetime to fraction of day.

    Parameters:
    df (pandas.DataFrame): The DataFrame to process.
    columns (list): List of column names to convert.

    Returns:
    pandas.DataFrame: The DataFrame with time columns converted.
    """
    for col in columns:
        if col in df.columns:
            df[col] = df[col].apply(datetime_to_day_fraction)
            # print(f'{col} complete')  
    return df

def create_utc_floats(df, dep_day_col = 'Dep Day', std_col = 'STD', blk_hrs_col = 'Blk Hrs'):
    """
    Adds UTC Departure and Arrival Float columns to the given DataFrame.

    Parameters:
    df (pandas.DataFrame): The DataFrame to process.
    dep_day_col (str): Column name for Departure Day.
    std_col (str): Column name for Scheduled Time of Departure.
    blk_hrs_col (str): Column name for Block Hours.

    Returns:
    pandas.DataFrame: The DataFrame with added UTC float columns.
    """
    if dep_day_col in df.columns and std_col in df.columns:
        df['UTC Dep Float'] = df[dep_day_col] + df[std_col]

    if 'UTC Dep Float' in df.columns and blk_hrs_col in df.columns:
        df['UTC Arr Float'] = df['UTC Dep Float'] + df[blk_hrs_col]

    return df
