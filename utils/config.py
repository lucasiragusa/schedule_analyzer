# Configuration parameters for the application

import pendulum

HUB = 'NUM'

# Example parameters for airport connections
# INput is in minuntes, divided by 1440 to get a fraction of a day

MIN_CONNECT_TIME = 60/1440  # in minutes
MAX_CONNECT_TIME = 240/1440  # in minutes
MAX_MISSED_CONNECT_TIME = -120/1440  # in minutes

# Maximum circuity allowed
MAX_CIRCUITY = 1.5 #multiple of the direct distance
MAX_ABS_CIRCUITY = 1200 #in km

 #Reference date to apply Daylight Savings Time
REF_DATE = pendulum.now().date()

# Time columns that need to be converted to fraction of day 
time_columns = ['STD', 'STA', 'DLcl', 'ALcl', 'Blk Hrs']
