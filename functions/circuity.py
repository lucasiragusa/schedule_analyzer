
from functools import lru_cache
from collections import OrderedDict
from .distance import great_circle_distance
from .import_data import import_airport_data

@lru_cache(maxsize=None)  # Infinite cache size. Adjust as needed.
def circuity(airport1, airport2, hub, airport_data = import_airport_data()):
    direct_distance = great_circle_distance(airport1, airport2, airport_data)
    total_distance = great_circle_distance(airport1, hub, airport_data) + great_circle_distance(hub, airport2, airport_data)
    return total_distance/direct_distance

@lru_cache(maxsize=None)  # Infinite cache size. Adjust as needed.
def absolute_circuity(airport1, airport2, hub,  airport_data = import_airport_data()):
    direct_distance = great_circle_distance(airport1, airport2, airport_data)
    total_distance = great_circle_distance(airport1, hub, airport_data) + great_circle_distance(hub, airport2, airport_data)
    return total_distance - direct_distance

# if __name__ == '__main__':
        
#     # Test circuity functions
#     print (circuity('SFO', 'JFK', 'LAX'))
#     print (absolute_circuity('SFO', 'JFK', 'LAX'))
    