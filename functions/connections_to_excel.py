import pandas as pd
import os
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from utils.config import HUB, MAX_CIRCUITY, MAX_ABS_CIRCUITY, MAX_MISSED_CONNECT_TIME, MIN_CONNECT_TIME, MAX_CONNECT_TIME

def export_connections_to_excel(
    df_connections, 
    df_missed_connections, 
    df_illogical_connections, 
    min_connect_time = MIN_CONNECT_TIME, 
    max_connect_time = MAX_CONNECT_TIME, 
    max_missed_time = MAX_MISSED_CONNECT_TIME, 
    max_circuity = MAX_CIRCUITY, 
    max_abs_circuity = MAX_ABS_CIRCUITY, 
    filename='Output/Connections_builder_output.xlsx'):
    
    
    # Create Output directory if it doesn't exist
    output_dir = os.path.dirname(filename)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Calculate statistics
    tot_connections = len(df_connections)
    median_connect_time = df_connections['Connection Time (min)'].median()
    median_abs_circuity = df_connections['Circuity (abs)'].median()
    median_circuity = df_connections['Circuity x'].median()
    missed_connections = len(df_missed_connections)

    # Write to Excel
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        df_connections.to_excel(writer, sheet_name='Valid connections', index=False)
        df_missed_connections.to_excel(writer, sheet_name='Missed connections', index=False)
        df_illogical_connections.to_excel(writer, sheet_name='Illogical connections', index=False)

        # Create and format the cover page
        writer.book.create_sheet('Cover Page', 0)
        cover = writer.book['Cover Page']
        cover.sheet_view.showGridLines = False

        center_aligned = Alignment(horizontal='center', vertical='center')
        bold_font = Font(bold=True, size=14)
        italic_font = Font(italic=True)

        cover['A1'] = "Schedule Connectivity Statistics"
        cover['A1'].font = bold_font
        cover['A1'].alignment = center_aligned
        cover.merge_cells('A1:D1')

        cover['A3'] = "Valid Connections"
        cover['A3'].font = bold_font
        cover['B3'] = tot_connections

        cover['A4'] = "Median CT (Mins)"
        cover['A4'].font = bold_font
        cover['B4'] = round(median_connect_time, 0)

        cover['A5'] = "Median Circuity %"
        cover['A5'].font = bold_font
        cover['B5'] = f"{median_circuity-1:.0%}"

        cover['A6'] = "Median Circuity (km)"
        cover['A6'].font = bold_font
        cover['B6'] = round(median_abs_circuity, 0)

        cover['A7'] = "Missed Connections"
        cover['A7'].font = bold_font
        cover['B7'] = missed_connections

        cover['A11'] = "Parameters"
        cover['A11'].font = bold_font
        cover['A12'] = f"CTs are considered valid between {min_connect_time*1440:.0f} and {max_connect_time*1440:.0f} minutes"
        cover['A12'].font = italic_font
        cover['A13'] = f"CTs are considered missed between {max_missed_time*1440:.0f} and {min_connect_time*1440-1:.0f} minutes"
        cover['A13'].font = italic_font
        cover['A14'] = f"Circuity considered valid if not exceeding {max_circuity}x & {max_abs_circuity}km vs. direct GC distance"
        cover['A14'].font = italic_font
