from pymongo import MongoClient
import pymongo
import feedparser


client = MongoClient()
db = client.get_database("tremp_easy")
users = db.get_collection("users")
trips = db.get_collection("trips")
tremps = db.get_collection("tremps")


def add_tremp(trip_id, nb_passengers, driver_id, trempist_id):
    tremp_details = { 'trip_id' : trip_id, "trempist_id" : trempist_id, "nb_passengers" : nb_passengers}
    tremps.replace_one(tremp_details, tremp_details , upsert=True)
    trips.update_one({ "trip_id" : trip_id,
                       "$inc" : { "nb_passengers" : -nb_passengers}})



def add_user(user_id, user_first_name, user_last_name, phone_number):
    user_details = {"user_id": user_id, "user_first_name": user_first_name, "user_last_name": user_last_name,
                    "phone_number": phone_number}
    users.replace_one(user_details, user_details, upsert=True)


def add_trip(driver_id, departure, destination, date, hour, nb_passengers):
    try:
        user_id_match = list(db.users.find({"user_id":driver_id}))
        if len(user_id_match)!=1:
            raise ("can't add the trip, the driver doesnwt exist in users")
        else:
            trip_details = {"driver_id": driver_id, "departure": departure.lower().title().strip(), "destination": destination.lower().title().strip(),
                            "date": date, "hour":hour, "nb_passengers": nb_passengers.strip()}
        trips.replace_one(trip_details, trip_details, upsert=True)
    except:
        pass

def get_source_destination_list(from_where, to_where, date, nb_passengers):
    l =list(db.trips.find({"$and": [{"departure": from_where.lower().title().strip()},
                                    {"destination": to_where.lower().title().strip()},
                                    {"date": date },
                                    {"nb_pseengers" : {"$gte" : nb_passengers}}]}))
    print(l)

add_user("317767556", "Shani", "Ehrentreu", "0548523955")
add_user("317767886", "Dobora", "Belansi", "0504163232")
add_trip("317767556", "Beitar", "Yafo","12/11/2019", "13:30", "5" )
add_trip("317767776", "Heifa", "Jerusalem", "12/11/2019", "13:30", "5")
add_trip("317767556", "Beitar", "Jerusalem", "12/11/2019", "13:30", "1")
add_trip("317767886", "Lod", "Jerusalem", "12/11/2019", "13:30", "2")
add_trip("317767556", "Beitar", "Jerusalem", "12/11/2019", "13:30", "4")
get_source_destination_list("Beitar", "Jerusalem", "12/11/2019", "2")

