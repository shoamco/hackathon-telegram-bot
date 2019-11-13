import requests
# import db_functions
# from Excceptions import UnknownLocation, Time_Format_Error
import typing
import db_functions
from db_functions import add_user
import Excceptions


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


def place_validation(name: str):
    try:
        param = name.replace(" ", "%20")
        r = requests.get(f"https://nominatim.openstreetmap.org/search?q={param}&format=json")
        r.raise_for_status()
        data = r.json()
        if len(data) == 0:
            raise UnknownLocation(f"{name}")
    except UnknownLocation as e:
        return False
    return True


def validation_hour(hour: str):
    hours, minute = hour.split(':')
    try:
        return len(hour.split(':')) == 2 and 0 <= int(hours) < 24 and 0 <= int(minute) < 60
    except:
        return False


def insert_user(user_dict: dict):
    """   def add_user(user_id, user_first_name, user_last_name, phone_number, user_name): """
    """   ride: {'date': '2019-11-12', 'time': '8:30', 'source': 'Jerusalem', 'destination': 'haifa', 'place': '3'}"""
    """user: {'id': 586475104, 'first_name': 'Mickaël', 'last_name': 'Balensi', 'username': None}"""
    user_id, user_first_name, user_last_name, user_name, phone_number = user_dict.values()
    add_user(user_id, user_first_name, user_last_name, phone_number, user_name)


def insert_ride_to_db(data_dict: dict, driver_id):
    """{'date': '2019-11-13', 'time': '8:39', 'source': 'jERUSALEM', 'destination': 'HAIFA', 'place': '4'}"""
    date, hour, departure, destination, nb_passengers = data_dict.values()
    db_functions.add_trip(driver_id, departure, destination, date, hour, nb_passengers)
    dest_lat, dest_lon = geocode(destination)
    dep_lat, dep_lon = geocode(departure)
    db_functions.add_trip(driver_id, departure, destination, date, hour, nb_passengers)


def get_trips(trip_details: dict):
    """get_source_destination_list("Beitar", "Jerusalem", "12/11/2019", "2")"""
    date, time, from_where, to_where, nb_passengers = trip_details.values()
    from_lat, from_lon = geocode(from_where)
    to_lat, to_lon = geocode(to_where)

    return db_functions.get_source_destination_list(from_where, to_where, date, nb_passengers)
