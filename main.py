from functions.import_data import import_airport_data, import_schedule
from functions.explode_schedule import explode_schedule
from functions.data_enrich import add_movement_flag, add_day_eight
from functions.time_conversion import convert_time_columns_to_fraction, create_utc_floats
from functions.build_connections import build_and_filter_connections
from functions.connections_to_excel import export_connections_to_excel
from utils.config import HUB, time_columns
import time

#Main function

def main(): 
    
    # Import data
    airport_data = import_airport_data()
    df = import_schedule('data/schedule_v8.xlsx', sheet_name='2030')
    
    # Pre-process connections
    df = explode_schedule(df)
    df = add_movement_flag(df)
    df = add_day_eight(df)
    df = convert_time_columns_to_fraction(df, time_columns)
    df = create_utc_floats(df)
    
    df_logical_connections, df_missed_connections, df_illogical_connections = build_and_filter_connections(df)
    
    export_connections_to_excel (df_logical_connections, df_missed_connections, df_illogical_connections) 
            
if __name__ == "__main__":
    main()
