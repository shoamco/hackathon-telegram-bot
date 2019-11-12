import requests

#import db_functions
from Excceptions import UnknownLocation, Time_Format_Error


def place_validation(name):
    param ='%20'.join(name.split(' '))
    r = requests.get(f"https://nominatim.openstreetmap.org/search?q={param}&format=json")
    r.raise_for_status()  # will raise an exception for HTTp status code != 200
    data = r.json()
    if len(data) == 0:
        raise UnknownLocation(f"I don't know any {name}")
    return True


def geocode(name):
    param ='%20'.join(name.split(' '))
    r = requests.get(f"https://nominatim.openstreetmap.org/search?q={param}&format=json")
    r.raise_for_status()  # will raise an exception for HTTp status code != 200
    data = r.json()
    if len(data) == 0:
        raise Exception(f"I don't know any {name}")
    element = data[0]
    #print(element)
    return tuple([float(element['lat']), float(element['lon'])])


def validation_hour(hour:str):
    hours, minute = hour.split(':')
    if not (len(hour.split(':')) == 2 and 0 <= int(hours) < 60 and 0 <= int(minute)< 60):
        raise Time_Format_Error


def insert_user(user_dict):
    """{'id': 586475104, 'first_name': 'Mickaël', 'last_name': 'Balensi', 'username': None}"""



def get_rides(details_dict):
    """params"""
    #get_source_destination_list(from_where, to_where, date):


def insert_ride_to_db(data_dict, driver_id=''):
    """{'date': '2019-11-13', 'time': '8:39', 'source': 'jERUSALEM', 'destination': 'HAIFA', 'place': '4'}"""
    date, hour, departure, destination, nb_passengers = data_dict
    if place_validation(departure) and place_validation(destination) and validation_hour(hour):
        #db_functions.add_trip(driver_id, departure, destination, date, hour, nb_passengers)
        print()

