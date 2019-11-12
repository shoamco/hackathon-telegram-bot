from pymongo import MongoClient
client = MongoClient()
db = client.get_database("tremp_easy")
users = db.get_collection("users")
trips = db.get_collection("trips")
tremps = db.get_collection("tremps")


def add_user(user_id, user_first_name, user_last_name, phone_number):
    user_details = {"user_id": user_id, "user_first_name": user_first_name, "user_last_name": user_last_name,
                    "phone_number": phone_number}
    users.replace_one(user_details, user_details, upsert=True)


def add_trip(driver_id, departure, destination, date, hour, nb_passengers):
    try:
        number_of_passengers = int(nb_passengers.strip())
        user_id_match = list(db.users.find({"user_id":driver_id}))
        if len(user_id_match)!=1:
            raise ("can't add the trip, the driver doesnwt exist in users")
        else:
            trip_details = {"driver_id": driver_id, "departure": departure.lower().title().strip(), "destination": destination.lower().title().strip(),
                            "date": date, "hour":hour, "nb_passengers": number_of_passengers}
        trips.replace_one(trip_details, trip_details, upsert=True)
    except:
        pass

def get_source_destination_list(from_where, to_where, date, number_of_seats):
    relevent_trip_list =list(db.trips.find({"$and": [{"departure": from_where.lower().title().strip()},
                                    {"destination": to_where.lower().title().strip()},
                                    {"date": date },{"nb_passengers": {'$gte' : number_of_seats}}]}))
    for trip in relevent_trip_list:
        drivers_details = list(db.users.find({"user_id": trip['driver_id']}))
        trip['drivers_pNumber'] = drivers_details[0]['phone_number']
        print(drivers_details)


def add_tremp(drivers_id, passengers_id, trips_id, number_of_passengers):
    tremp_details = {"drivers_id": drivers_id, "passengers_id": passengers_id,
                    "trips_id": trips_id, "number_of_passengers": number_of_passengers}
    tremps.replace_one(tremp_details, tremp_details, upsert=True)
    trips_details = list(db.trips.find({"_id":trips_id}))
    print(trips_details)
    # old_number_of_passengers = trips_details[0]["nb_passengers"]
    # db.trips.updateOne({"_id": trips_id},
    #                    {"$set":{ "nb_passengers": old_number_of_passengers - int(number_of_passengers)}})
    #

add_user("317767556", "Shani", "Ehrentreu", "0548523955")
add_user("317767886", "Dobora", "Belansi", "0504163232")
add_trip("317767556", "Beitar", "Yafo","12/11/2019", "13:30", "5 ")
add_trip("317767776", "Heifa", "Jerusalem", "12/11/2019", "13:30", "5")
add_trip("317767556", "Beitar", "Jerusalem", "12/11/2019", "13:30", "1")
add_trip("317767886", "Lod", "Jerusalem", "12/11/2019", "13:30", "2")
add_trip("317767886", "Beitar", "Jerusalem", "12/11/2019", "13:30", "4")
get_source_destination_list("Beitar", "Jerusalem", "12/11/2019", "3")
add_tremp("317767886","333222111","5dca8955d21dacefda25e8c9", "2")
