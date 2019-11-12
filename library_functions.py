import requests
# import db_functions
# from Excceptions import UnknownLocation, Time_Format_Error
import typing

import db_functions
from db_functions import add_user


class UnknownLocation(Exception):
    def __init__(self, location):
        super().__init__(location)
        self.location = location

    def __str__(self):
        return repr(self.value)


def geocode(name_place: str) -> typing.Tuple[float, float]:
    """
   the function get a name of place,and return coordinates from place names using Nominatim
   :param name_place:name of place for searching
   :return: coordinates (x,y)
   """
    # search API for Jerusalem and return the first result by json,
    r = requests.get("https://nominatim.openstreetmap.org/search",
                     params={'q': name_place, 'format': 'json', 'limit': 1})
    r.raise_for_status()  # will raise an exception for HTTp status code != 200
    data = r.json()
    if not data:
        raise UnknownLocation(name_place)
    x, y = float(data[0]["lat"]), float(data[0]["lon"])
    return x, y


def place_validation(name):
    # param ='%20'.join(name.split(' '))
    # r = requests.get(f"https://nominatim.openstreetmap.org/search?q={param}&format=json")
    # r.raise_for_status()  # will raise an exception for HTTp status code != 200
    # data = r.json()
    # if len(data) == 0:
    #     raise UnknownLocation(f"{name}")
    try:
        geocode(name)
    except UnknownLocation as e:
        return False
    return True


# def validation_hour(hour:str):
#     hours, minute = hour.split(':')
#     if not (len(hour.split(':')) == 2 and 0 <= int(hours) < 60 and 0 <= int(minute)< 60):
#         raise Time_Format_Error
def validation_hour(hour: str):
    hours, minute = hour.split(':')
    return len(hour.split(':')) == 2 and 0 <= int(hours) < 60 and 0 <= int(minute) < 60


def insert_user(user_dict):
    """    def add_user(user_id, user_first_name, user_last_name, phone_number, user_name):
    """
    """   ride: {'date': '2019-11-12', 'time': '8:30', 'source': 'Jerusalem', 'destination': 'haifa', 'place': '3'}"""
    """user: {'id': 586475104, 'first_name': 'Mickaël', 'last_name': 'Balensi', 'username': None}"""
    user_id, user_first_name, user_last_name, phone_number ,user_name = user_dict  #=>>> ici yaura un pb car jai pas encore le num de telephone
    add_user(user_id, user_first_name, user_last_name, phone_number)

def get_rides(details_dict):
    """params"""
    # get_source_destination_list(from_where, to_where, date):


def insert_ride_to_db(data_dict:dict, driver_id):
    """{'date': '2019-11-13', 'time': '8:39', 'source': 'jERUSALEM', 'destination': 'HAIFA', 'place': '4'}"""
    date, hour, departure, destination, nb_passengers = data_dict.values()
    if place_validation(departure) and place_validation(destination) and validation_hour(hour):
        db_functions.add_trip(driver_id, departure, destination, date, hour, nb_passengers)

