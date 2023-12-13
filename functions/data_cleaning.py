import pandas as pd
from collections import OrderedDict
import re

def clean_frequency(column):
    """
    Cleans the specified column Series by replacing ellipses with periods,
    removing all non-numeric characters, and formatting the string so that
    it contains numbers from 1 to 7 or a dot in their place if the number is not present.

    Parameters:
    column (pandas.Series): The Series to be cleaned and formatted.

    Returns:
    pandas.Series: The cleaned and formatted Series.
    """
    def format_string(s):
        # Replace ellipses with periods and remove all non-numeric characters
        cleaned = re.sub(r'[^\d]', '', s.replace('…', '.'))
        
        # Construct a 7-character string with numbers 1-7 or dots
        formatted = ''.join(str(i) if str(i) in cleaned else '.' for i in range(1, 8))
        return formatted

    return column.astype(str).apply(format_string)
