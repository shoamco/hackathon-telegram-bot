from bson import ObjectId
from pymongo import MongoClient
from datetime import datetime, timedelta
import pymongo
import feedparser


def create_tremp_easy_data_base():
    client = MongoClient()
    db = client.get_database("tremp_easy")
    users = db.get_collection("users")
    trips = db.get_collection("trips")
    tremps = db.get_collection("tremps")
    return db, users, trips, tremps


def add_tremp(trip_id, nb_passengers,  trempist_id):
    db, users, trips, tremps = create_tremp_easy_data_base()
    nb_passengers = int(nb_passengers)
    trip_choosen = db.trips.find_one({"_id" : ObjectId(trip_id)})

    # 1 => take details from driver
    #driver_id = str(trip_choosen["driver_id"])
    driver_details = list(db.users.find({"user_id" : trip_choosen["driver_id"]}))
    driver_details = db.users.find_one({"user_id" : trip_choosen["driver_id"]})

    #2 => add tremp record to the table
    tremp_details = { 'trip_id' : trip_id, "trempist_id" : trempist_id, "nb_passengers" : nb_passengers}
    tremps.replace_one(tremp_details, tremp_details , upsert=True)

    #3 => update available seats
    trips.update_one({"_id" : ObjectId(trip_id)}, {"$inc" : { "nb_passengers" : -nb_passengers}})

    return driver_details


def add_user(user_id, user_first_name, user_last_name, phone_number, user_name):
    db, users, trips, tremps = create_tremp_easy_data_base()

    user_details = {"user_id": user_id, "user_first_name": user_first_name, "user_last_name": user_last_name,
                    "phone_number": phone_number, "user_name":user_name}
    users.replace_one(user_details, user_details, upsert=True)


def add_trip(driver_id, departure, destination, date, hour, nb_passengers):
    db, users, trips, tremps = create_tremp_easy_data_base()
    #driver_id = str(driver_id)
    try:
        number_of_passengers = int(nb_passengers.strip())
        result_driver_find = db.users.find({"user_id": driver_id})
        result_list = list(result_driver_find)
        if len(result_list) != 1:
            raise Exception("can't add the trip, the driver doesn't exist in users")
        else:
            trip_details = {"driver_id": driver_id, "departure": departure.lower().title().strip(), "destination": destination.lower().title().strip(),
                            "date": date, "hour":hour, "nb_passengers": number_of_passengers}
        trips.replace_one(trip_details, trip_details, upsert=True)
    except:
        pass


def get_source_destination_list(from_where, to_where, date, nb_passengers):
    db, users, trips, tremps = create_tremp_easy_data_base()
    number_of_passengers = int(nb_passengers.strip())
    trips_results =list(db.trips.find({"$and": [{"departure": from_where.lower().title().strip()},
                                    {"destination": to_where.lower().title().strip()},
                                    {"date": date },
                                    {"nb_passengers": {"$gte": number_of_passengers}},
                                    {"nb_passengers": {"$gte": 0}}]}))

    return (trips_results)


def check_if_up_to_hour_diffrence (date1, date2):
    db, users, trips, tremps = create_tremp_easy_data_base()
    pass


def get_source_destination_list_hours(from_where, to_where, date, hour, nb_passengers):
    db, users, trips, tremps = create_tremp_easy_data_base()
    hour = hour + ":00"
    datetime_object = datetime.strptime(date + " " + hour, '%Y-%m-%d %H:%M:%S')
    number_of_passengers = int(nb_passengers.strip())
    trips_results =list(db.trips.find({"$and": [{"departure": from_where.lower().title().strip()},
                                    {"destination": to_where.lower().title().strip()},
                                    {"date": date },
                                    {"nb_passengers" : {"$gte" : number_of_passengers},}]}))
    return (trips_results)