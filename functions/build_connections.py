import pandas as pd
from functions.data_cleaning import clean_frequency
from functions.circuity import circuity, absolute_circuity
from utils import config
from .distance import haversine, great_circle_distance


def build_and_filter_connections(
    df, 
    max_circuity = config.MAX_CIRCUITY, 
    max_abs_circuity = config.MAX_ABS_CIRCUITY, 
    max_missed_time = config.MAX_MISSED_CONNECT_TIME, 
    min_connect_time = config.MIN_CONNECT_TIME, 
    max_connect_time = config.MAX_CONNECT_TIME
    ):
    """
    Builds connections between arrival and departure dataframes, and filters for logical, illogical, and missed connections.

    Parameters:
    df_arr (pandas.DataFrame): DataFrame of arrivals.
    df_dep (pandas.DataFrame): DataFrame of departures.
    max_circuity (float): Maximum allowed circuity.
    max_abs_circuity (float): Maximum allowed absolute circuity.
    max_missed_time (float): Maximum time for a connection to be considered missed.
    min_connect_time (float): Minimum connection time for a feasible connection.
    max_connect_time (float): Maximum connection time for a feasible connection.

    Returns:
    tuple: A tuple containing DataFrames for logical connections, illogical connections, and missed connections.
    """

    # Split the main df into arrivals and departures 
    df_arr = df[df['movement_flag'] == 'Arr']
    df_dep = df[df['movement_flag'] == 'Dep']
    
    # Merge the arrival and departure dataframes
    df_connections = pd.merge(left=df_arr, right=df_dep, how='left', 
                              left_on='Dest', right_on='Orig', 
                              suffixes=('_arr', '_dep'))

    # Calculate connection time and circuity
    df_connections['Connection_time'] = df_connections['UTC Dep Float_dep'] - df_connections['UTC Arr Float_arr']
    df_connections['Circuity'] = df_connections.apply(lambda row: circuity(row['Orig_arr'], row['Dest_dep'], row['Dest_arr']), axis=1)
    df_connections['Circuity (abs)'] = df_connections.apply(lambda row: absolute_circuity(row['Orig_arr'], row['Dest_dep'], row['Dest_arr']), axis=1)

    # Remove connections that depart and arrive at the same station
    df_connections = df_connections[df_connections['Orig_arr'] != df_connections['Dest_dep']]

    # Identify illogical but feasible connections
    df_illogical_connections = df_connections[(df_connections['Connection_time'] >= min_connect_time) & 
                                              (df_connections['Connection_time'] <= max_connect_time) & 
                                              ((df_connections['Circuity'] > max_circuity) | 
                                               (df_connections['Circuity (abs)'] > max_abs_circuity))]

    # Save geographically logical but missed connections
    df_missed_connections = df_connections[(df_connections['Connection_time'] >= max_missed_time) & 
                                           (df_connections['Connection_time'] < min_connect_time) & 
                                           (df_connections['Circuity'] <= max_circuity) & 
                                           (df_connections['Circuity (abs)'] <= max_abs_circuity)]

    # Filter for feasible and logical connections
    df_logical_connections = df_connections[(df_connections['Connection_time'] >= min_connect_time) & 
                                            (df_connections['Connection_time'] <= max_connect_time) & 
                                            ((df_connections['Circuity'] <= max_circuity) |
                                            (df_connections['Circuity (abs)'] <= max_abs_circuity))]

    print (f'Number of logical connections: {len(df_logical_connections)}')
    print (f'Number of illogical connections: {len(df_illogical_connections)}')
    print (f'Number of missed connections: {len(df_missed_connections)}')

    # Define new column names
    new_cols_name = {
        'Aln_arr' : 'Inbound Airline', 
        'Flt_arr' : 'Inbound Flt no', 
        'Orig_arr' : 'Inbound Orig Airp', 
        'STD_arr' : 'Inbound STD (UTC)',
        'DLcl_arr' : 'Inbound STD (Local)', 
        'Dest_arr' : 'Via',
        'STA_arr' : 'Inbound STA (UTC)', 
        'ALcl_arr' : 'Inbound STA (Local)', 
        'Blk Hrs_arr' : 'Inbound Block Hrs', 
        'Dep Day_arr' : 'Inbound Dep Day (UTC)', 
        'Subfl_arr' : 'Inbound Equip',
        'Seats_arr' : 'Inbound Seats',
        # 'Traffic Restrictions (if any)_arr', 
        # 'Market_arr' 
        # 'movement_flag_arr', 
        'UTC Dep Float_arr' :'Inbound Dep Float',
        'UTC Arr Float_arr' : 'Inbound Arr Float',
        'Aln_dep' : 'Outbound Airline',
        'Flt_dep' : 'Outbound Flt no',
        # 'Orig_dep' : 'Outbound Orig Airp',
        'STD_dep' : 'Outbound STD (UTC)',
        'DLcl_dep' : 'Outbound STD (Local)',
        'Dest_dep' : 'Outbound Dest Airp',
        'STA_dep' : 'Outbound STA (UTC)',
        'ALcl_dep' : 'Outbound STA (Local)',
        'Blk Hrs_dep' : 'Outbound Block Hrs',
        'Dep Day_dep' : 'Outbound Dep Day (UTC)',
        'Subfl_dep' : 'Outbound Equip',
        'Seats_dep' : 'Outbound Seats',
        # 'Traffic Restrictions (if any)_dep', 
        # 'Market_dep',
        # 'movement_flag_dep', 
        'UTC Dep Float_dep' : 'Outbound Dep Float', 
        'UTC Arr Float_dep' : 'Outbound Arr Float',
        'Connection_time' : 'Connection Time (min)',
        'Circuity' : 'Circuity x',
        'Circuity (abs)' : 'Circuity (abs)',
    }

    # Rename columns in all DataFrames
    df_logical_connections = rename_connection_columns(df_logical_connections, new_cols_name)
    df_illogical_connections = rename_connection_columns(df_illogical_connections, new_cols_name)
    df_missed_connections = rename_connection_columns(df_missed_connections, new_cols_name)
    
    # Make sure that the day 8 appear as D1s 
    for df in [df_logical_connections, df_illogical_connections, df_missed_connections]: 
        df['Inbound Dep Day (UTC)'] = df['Inbound Dep Day (UTC)'].apply(lambda x: 1 if x == 8 else x)
        df['Outbound Dep Day (UTC)'] = df['Outbound Dep Day (UTC)'].apply(lambda x: 1 if x == 8 else x)
        
    # Remove duplicates in all DataFrames
    df_logical_connections = df_logical_connections.drop_duplicates()
    df_illogical_connections = df_illogical_connections.drop_duplicates()
    df_missed_connections = df_missed_connections.drop_duplicates()

    # Group everything in compact form
    group_columns = [col for col in df_logical_connections.columns if col not in [
        'Inbound Dep Day (UTC)', 
        'Outbound Dep Day (UTC)', 
        'Inbound Dep Float', 
        'Inbound Arr Float', 
        'Outbound Dep Float',
        'Outbound Arr Float'
    ]]
    
    dfs = [df_logical_connections, df_missed_connections, df_illogical_connections]
    print ('Copying to clipboard')

    # df_logical_connections.to_clipboard(index=False)
    print(f'logical connectionsL {len(df_logical_connections)}')

    # Perform groupby aggregation so that every flight with the same descriptors is rolled out on the same row

    for i, df in enumerate(dfs):
        df['Inbound Dep Day (UTC)'] = df['Inbound Dep Day (UTC)'].astype(str)
        df['Outbound Dep Day (UTC)'] = df['Outbound Dep Day (UTC)'].astype(str)

        df_agg = df.groupby(group_columns).agg({
            'Inbound Dep Day (UTC)': lambda x: ''.join(x), 
            'Outbound Dep Day (UTC)': lambda x: ''.join(x)
        }).reset_index()

        # Apply functions to remove duplicates and sort strings
        # df_agg['Inbound Dep Day (UTC)'] = clean_frequency(df_agg['Inbound Dep Day (UTC)'])
        # df_agg['Outbound Dep Day (UTC)'] = clean_frequency(df_agg['Outbound Dep Day (UTC)'])

        dfs[i] = df_agg

    return dfs[0], dfs[1], dfs[2]

def rename_connection_columns(df, new_columns_mapping):
    """
    Renames columns of the DataFrame based on the provided mapping.

    Parameters:
    df (pandas.DataFrame): The DataFrame whose columns are to be renamed.
    new_columns_mapping (dict): A dictionary mapping old column names to new names.

    Returns:
    pandas.DataFrame: The DataFrame with renamed columns.
    """
    df = df.rename(columns=new_columns_mapping)
    return df[new_columns_mapping.values()]

