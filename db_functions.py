from bson import ObjectId
from pymongo import MongoClient
from datetime import datetime

import pymongo
import feedparser


client = MongoClient()
db = client.get_database("tremp_easy")
users = db.get_collection("users")
trips = db.get_collection("trips")
tremps = db.get_collection("tremps")


def add_tremp(trip_id, nb_passengers,  trempist_id):
    nb_passengers = int(nb_passengers)
    trip_choosen = db.trips.find_one({"_id" : ObjectId(trip_id)})
    print(trip_choosen)
    # trip_choosen = trip_choosen[0]
    # print(trip_choosen)

    # 1 => take details from driver
    driver_details = list(db.users.find({"user_id" : trip_choosen["driver_id"]}))
    phone_number = driver_details[0]["phone_number"]
    name = driver_details[0]["user_first_name"] + " " + driver_details[0]["user_last_name"]

    #2 => add tremp record to the table
    tremp_details = { 'trip_id' : trip_id, "trempist_id" : trempist_id, "nb_passengers" : nb_passengers}
    tremps.replace_one(tremp_details, tremp_details , upsert=True)

    #3 => update available seats
    trips.update_one({"_id" : ObjectId(trip_id)},
                     {"$inc" : { "nb_passengers" : -nb_passengers}})
    print(name)
    print(driver_details)
    print(phone_number)

    return name, phone_number


def add_user(user_id, user_first_name, user_last_name, phone_number, user_name):
    user_details = {"user_id": user_id, "user_first_name": user_first_name, "user_last_name": user_last_name,
                    "phone_number": phone_number, "user_name":user_name}
    users.replace_one(user_details, user_details, upsert=True)


def add_trip(driver_id, departure, destination, date, hour, nb_passengers):
    try:
        number_of_passengers = int(nb_passengers.strip())
        result_driver_find = db.users.find({"user_id":driver_id})
        result_list = list(result_driver_find)
        #user_id_match = list()
        if len(result_list)!=1:
            raise ("can't add the trip, the driver doesnwt exist in users")
        else:
            trip_details = {"driver_id": driver_id, "departure": departure.lower().title().strip(), "destination": destination.lower().title().strip(),
                            "date": date, "hour":hour, "nb_passengers": number_of_passengers}
        trips.replace_one(trip_details, trip_details, upsert=True)
    except:
        pass

def get_source_destination_list(from_where, to_where, date, nb_passengers):
    number_of_passengers = int(nb_passengers.strip())
    trips_results =list(db.trips.find({"$and": [{"departure": from_where.lower().title().strip()},
                                    {"destination": to_where.lower().title().strip()},
                                    {"date": date },
                                    {"nb_passengers" : {"$gte" : number_of_passengers}}]}))

    return (trips_results)




def get_source_destination_list_hours(from_where, to_where, date, hour, nb_passengers):
    hour = hour + ":00"
    datetime_object = datetime.strptime(date + hour, '%y-%m-%d %H:%M:%S')
    print(datetime_object)
    number_of_passengers = int(nb_passengers.strip())
    trips_results =list(db.trips.find({"$and": [{"departure": from_where.lower().title().strip()},
                                    {"destination": to_where.lower().title().strip()},
                                    {"date": date },
                                    {"nb_passengers" : {"$gte" : number_of_passengers}}]}))

    return (trips_results)

"""
users.delete_many({})
trips.delete_many({})
tremps.delete_many({})"""
# add_user("317767556", "Shani", "Ehrentreu", "0548523955", "@shani")
# add_user("317767886", "Dobora", "Belansi", "0504163232", "@debora")
# add_trip("317767556", "Beitar", "Yafo","12/11/2019", "13:30", "5" )
# add_trip("317767776", "Heifa", "Jerusalem", "12/11/2019", "13:30", "5")
# add_trip("317767556", "Beitar", "Jerusalem", "12/11/2019", "13:30", "1")
# add_trip("317767886", "Lod", "Jerusalem", "12/11/2019", "13:30", "2")
# add_trip("317767556", "Beitar", "Jerusalem", "12/11/2019", "13:30", "4")
# get_source_destination_list("Beitar", "Jerusalem", "12/11/2019", "2")
#
# add_tremp("5dcaae01d21dacefda25f4b4" , "2" , "317767556")
date = "2019-11-12"
hour = "23:15"
hour = hour + ":00"
print (date + " " + hour)
datetime_object = datetime.strptime(date + " " + hour, '%y-%m-%d %H:%M:%S')
print(datetime_object)