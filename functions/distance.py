import math
import numpy as np


# Define distance functions
def haversine(lat1, lon1, lat2, lon2):    
    R = 6371 # Radius of the earth in km
    lat1, lon1, lat2, lon2 = map(np.deg2rad, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    return R * c

def great_circle_distance(airport1, airport2, airport_data):
    
    '''Returns the great circle distance between two airports in km'''
    
    lat1, lon1 = airport_data[airport1]['Latitude'], airport_data[airport1]['Longitude']
    lat2, lon2 = airport_data[airport2]['Latitude'], airport_data[airport2]['Longitude']
    return haversine(lat1, lon1, lat2, lon2)
