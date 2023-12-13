
import pandas as pd

def import_airport_data (): 
    
    """Imports airport data from pkl file and returns a dictionary dataframe"""
    airport_data = pd.read_pickle("data/airport_data.pkl")
    return airport_data


def import_schedule(path_to_schedule, sheet_name=None):
    
    """Imports schedule data from excel file or csv file and returns a dataframe"""
    
    if path_to_schedule.endswith('.csv'):
        schedule_data = pd.read_csv(path_to_schedule)
    elif path_to_schedule.endswith('.xlsx') or path_to_schedule.endswith('.xls'):
        try:
            schedule_data = pd.read_excel(path_to_schedule, sheet_name=sheet_name)
        except ValueError:
            raise ValueError(f"Sheet '{sheet_name}' does not exist in the Excel file.")
    else:
        raise ValueError("Invalid file format. Only CSV and Excel files are supported.")
    return schedule_data

