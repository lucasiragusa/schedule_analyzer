import pandas as pd

def explode_schedule(df, col_name = 'Dep Day'):
    """
    Transforms the 'Dep Day' column of a DataFrame by converting it into a list of integers,
    and then explodes the DataFrame based on this column.

    Args:
    df (pd.DataFrame): The input DataFrame with a 'Dep Day' column.

    Returns:
    pd.DataFrame: A new DataFrame with the 'Dep Day' column exploded.
    """
    # Ensure 'Dep Day' is a string column
    df[col_name] = df[col_name].astype(str)

    # Create a list of numbers from the 'Dep Day' string, excluding '.'
    df[col_name] = df[col_name].apply(lambda x: [int(num) for num in x if num.isdigit()])

    # Explode the DataFrame on 'Dep Day' to create separate rows for each day
    df_exploded = df.explode(col_name)

    return df_exploded

# if __name__ == '__main__': 
    
#     test = pd.DataFrame({'Dep Day': ['1.', '2.4', '3.5']})
#     print(explode_schedule(test))
    